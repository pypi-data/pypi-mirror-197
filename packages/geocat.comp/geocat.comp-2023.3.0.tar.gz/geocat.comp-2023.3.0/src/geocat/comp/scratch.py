from src.geocat.comp.climatologies import climatology_average#, _subset_by_season

import pandas as pd
import xskillscore as xs
import xarray as xr
import numpy as np
import time

def create_data(n_lat, n_lon, n_time):
    lat = np.linspace(-90, 90, n_lat)
    lon = np.linspace(-180, 180, n_lon)
    time = pd.date_range('2022-01-01', freq='M', periods=n_time)
    temp = 28 + 3 * np.random.randn(n_lon, n_lat, n_time)

    ds = xr.Dataset(data_vars=dict(
                        temp=(['lon', 'lat', 'time'], temp)),
                    coords=dict(
                        lon=lon,
                        lat=lat,
                        time=time,
                    ),
                    attrs=dict(description='Toy Weather Data'))
    return ds

def climate_tests():
    # load example dataset and create monthly means
    air = xr.tutorial.open_dataset("air_temperature")
    air_month = air.resample(time="M").mean()

    # find months belonging to season
    DJF = air_month.time.dt.month.isin([12, 1, 2])
    MAM = air_month.time.dt.month.isin([3, 4, 5])
    JJA = air_month.time.dt.month.isin([6, 7, 8])
    SON = air_month.time.dt.month.isin([9, 10, 11])

    concat_dim = xr.DataArray(["DJF", "MAM", "JJA", "SON"], dims="season")

    seasons = xr.concat([DJF, MAM, JJA, SON], dim=concat_dim)

    # calc mean over seasons
    result = xr.dot(air_month.air, seasons).transpose('season', 'lat', 'lon')
    expected = climatology_average(air.air, 'season')
    xr.testing.assert_allclose(result, expected)

# Test for https://github.com/NCAR/geocat-comp/issues/345
'''
import src.geocat.comp as gc

dattest = xr.open_dataset('dattest.nc')
phis_era5_rg = xr.open_dataset('dattest_phis.nc').isel({'lat':0, 'lon':0})
print(dattest.compute())
tinterp = gc.interpolation.interp_hybrid_to_pressure(
    dattest.T, dattest.PS, dattest.a_model, dattest.b_model, p0=1e5, method='log', lev_dim='lev', extrapolate=True,
     variable='temperature', t_bot = dattest.TBOT, phi_sfc = phis_era5_rg.__xarray_dataarray_variable__)

print(tinterp.compute())
#'''

climate_tests()
