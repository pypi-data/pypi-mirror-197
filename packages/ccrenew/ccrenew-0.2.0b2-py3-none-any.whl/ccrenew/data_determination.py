from __future__ import annotations
from collections.abc import Callable
import functools
from numbers import Number
import pandas as pd
from pvlib.location import Location
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.stats import gmean
from scipy.signal import find_peaks
from statistics import geometric_mean
from typing import TypedDict
from typing_extensions import Unpack

from ccrenew import DaylightParams

class SensorData(TypedDict):
    df: pd.DataFrame
    project_params: DaylightParams

def daylight(func: Callable):
    @functools.wraps(func)
    def calc_daylight_hours(**kwargs: Unpack[SensorData]):
        # Collect df & project to determine daylight hours
        df = kwargs.get('df')
        project_params = kwargs.get('project_params')

        # Calculate daylight hours
        lat = project_params.lat
        lon = project_params.lon
        tz = project_params.tz
        project_location = Location(lat, lon, tz)
        times = df.index.tz_localize(tz) # type: ignore
        df_suntimes = project_location.get_sun_rise_set_transit(times, method='spa')[['sunrise', 'sunset']]
        df_suntimes.index = pd.DatetimeIndex(df_suntimes.index)
        df = df.loc[df_suntimes.query("index.dt.hour >= sunrise.dt.hour and index.dt.hour <= sunset.dt.hour").index.tz_localize(None)] # type: ignore
        kwargs['df'] = df

        # Pass df with only daylight hours to the function
        result = func(**kwargs)
        return result
    return calc_daylight_hours

def comms(df: pd.DataFrame)-> pd.DataFrame:
    return df.isnull()

def zeroes(df: pd.DataFrame) -> pd.DataFrame:
    return df == 0

@daylight
def daylight_zeroes(*, df: pd.DataFrame, project_params: DaylightParams) -> pd.DataFrame:
    """
    Return zero values during daylight hours.

    Args:
        df (pd.DataFrame): Dataframe of project readings.
        project_params (DaylightParams): A namedtuple object with parameters for calculating daylight hours.

    Returns:
        pd.DataFrame A set of bool values based on zeroes.
    """
    return zeroes(df)

def frozen(df: pd.DataFrame, window: str|int|None = None) -> pd.DataFrame:
    """ 'cutoff_limit' is minimum amount of time values must be unchanged to be considered frozen. 
    This parameters can be provided in the ContractParameters class in the config script. 
    The default is to use the minimum timedelta found in the DAS data."""
    if not window:
        return (df != 0) & (df.diff() == 0)
    if isinstance(window, str):
        df_freq = pd.infer_freq(df.index) # type: ignore
        window_range = 2*pd.Timedelta(window) - pd.Timedelta(df_freq) # type: ignore
        window_range = window_range/df_freq # type: ignore
    elif isinstance(window, Number):
        window_range = window
    else:
        raise TypeError('cutoff_limit for frozen values must be a number representing window size or a string in format ##min')
    
    lookback = df.rolling(window=window_range).apply(lambda x: np.all(x==x[0]), raw=True)
    forward_indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=window_range)
    lookforward = df.rolling(window=forward_indexer).apply(lambda x: np.all(x==x[0]), raw=True)
    frozen = lookback.fillna(0) + lookforward.fillna(0)

    return frozen > 0

def frozen_center(df: pd.DataFrame, window: str|int|None = None) -> pd.DataFrame:
    """ 'cutoff_limit' is minimum amount of time values must be unchanged to be considered frozen. 
    This parameters can be provided in the ContractParameters class in the config script. 
    The default is to use the minimum timedelta found in the DAS data.  """
    if not window:
        return (df != 0) & (df.diff() == 0)
    if isinstance(window, str):
        df_freq = pd.infer_freq(df.index) # type: ignore
        window_range = 2*pd.Timedelta(window) - pd.Timedelta(df_freq) # type: ignore
    elif isinstance(window, Number):
        window_range = window
    else:
        raise TypeError('cutoff_limit for frozen values must be a number representing window size or a string in format ##min')

    frozen = df.rolling(window_range, center=True).apply(lambda x: np.all(x == x[0]), raw=True) # type: ignore

    return frozen == 1

@daylight
def daylight_frozen(*, df: pd.DataFrame, project_params: DaylightParams, window: str|int|None = None) -> pd.DataFrame:
    return frozen(df, window)

def negatives(df: pd.DataFrame, cols: list=[]) -> pd.DataFrame:
    df = df.copy()
    if cols:
        df = df[cols] < 0
    else:
        df = df <0
    return df

def decreasing(df: pd.DataFrame) -> pd.DataFrame:
    return df.diff() < 0

def band_pass(df: pd.DataFrame, col_limits: list[tuple]) -> pd.DataFrame:
    df=df.copy()
    for col, limits in col_limits:
        df.loc[:,col] = (df[col].lt(limits[0])) | (df[col].gt(limits[1]))

    return df

def poa_mistracking(df: pd.DataFrame, degree: int=8) -> pd.DataFrame:
    df = df.copy()
    for day, df_daily in df.groupby(df.index.date): # type: ignore
        x = df_daily.index.hour

        # Find peaks for Solcast data
        y_solcast_raw = df_daily['Solcast']
        y_solcast = y_solcast_raw.fillna(0)
        fit_solcast = np.poly1d(np.polyfit(x, y_solcast, degree))

        x_fit = np.linspace(x[0], x[-1], 100)
        y_fit_solcast = fit_solcast(x_fit)

        # Count the number of hours that are above half the maximum value for the series
        # Trackers will have more hours above this value than non-trackers
        count_max_50_solcast = (y_solcast>y_solcast_raw.max()/2).sum()
        max_66_solcast = y_solcast_raw.max()*2/3

        # Only consider peaks that are at least 2/3rds as high as the maximum
        peaks_solcast, _ = find_peaks(y_fit_solcast, height=max_66_solcast)
        peak_count_solcast = len(peaks_solcast)


        # Loop through POA columns to find peaks
        for col in df.columns[df.columns != 'Solcast']:
            y_raw = df_daily[col]
            y = y_raw.fillna(0)
            fit = np.poly1d(np.polyfit(x, y, degree))

            x_fit = np.linspace(x[0], x[-1], 100)
            y_fit = fit(x_fit)

            # Calculate % of max values for use in calculations
            count_max_50 = (y_raw>y_raw.max()/2).sum()
            max_66 = y_raw.max()*2/3

            # Only consider peaks that are at least 2/3rds as high as the maximum
            peaks, _ = find_peaks(y_fit, height=max_66)
            peak_count = len(peaks)

            # If only 1 peak & Solcast shows more than 1, we'll consider it mistracking
            # If the number of points above 50% max for Solcast vs Native is 2 or more, we'll consider it mistracking
            if peak_count < 2 and peak_count_solcast >= 2:
                df.loc[df.index.date==day, col] = True # type: ignore
            elif count_max_50_solcast - count_max_50 > 1:
                df.loc[df.index.date==day, col] = True # type: ignore
            else:
                df.loc[df.index.date==day, col] = False # type: ignore

    df = df.drop(columns='Solcast').astype(bool)

    return df

@daylight
def daylight_poa_mistracking(*, df: pd.DataFrame, project_params: DaylightParams, degree: int=8):
    return poa_mistracking(df, degree)

def spline_filter(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df_bool = ~df.isna()
    for col in df.columns:
        non_nulls = df[col][df[col].notna()]
        x = non_nulls.index.values.astype('float')
        y = non_nulls.values
        cs = CubicSpline(x, y)
        deriv = cs(x, 1)
        deriv_mean = np.mean(deriv)
        stdev = np.std(deriv)
        y = (deriv < -2.5*stdev) | (deriv > 2.5*stdev)
        bool_col = pd.DataFrame(index=pd.to_datetime(x), data={col: y})
        df_bool.update(bool_col)
    df_bool = df_bool.astype(bool)

    return df_bool


if __name__ == '__main__':
    dates = pd.date_range('2023-1-1 00:00', '2023-6-1 00:00', freq='5T')
    values = list(range(len(dates)))

    data = np.array([values, values, values, values, values]).T
    df = pd.DataFrame(index=dates, data=data)
    df.loc[df.index < '2023-01-01 00:10'] = 1
    df.loc[(df.index > '2023-01-01 00:20') & (df.index < '2023-01-01 01:00')] = 1
    df.loc[(df.index > '2023-01-01 01:10') & (df.index < '2023-01-01 01:40')] = -1
    s = df.iloc[:,[0]]
    frozen(s, '15T')