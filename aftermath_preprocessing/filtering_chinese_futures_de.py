import pandas as pd
import numpy as np
from tools import featGen
from scipy.stats.mstats import zscore, winsorize
import swifter
import os
pd.set_option('display.max_colwidth', -1)  # or 199
pd.set_option('display.max_columns', None)  # or 1000


print(os.getcwd())
try:
    china_futures = pd.read_pickle("data/china_futures_20191019.pkl")
except FileNotFoundError:
    china_futures = pd.read_csv("data/DY_FUA_88508ff2d98f32716f2eae24114c73df.csv")
    china_futures.to_pickle("data/china_futures_20191019.pkl")
    china_futures = pd.read_pickle("data/china_futures_20191019.pkl")



china_futures.date = pd.to_datetime(china_futures.date)
china_futures.index = china_futures.date
china_futures = china_futures.sort_index()

china_futures_close = china_futures[['close', 'commodity']]

china_futures_close = pd.pivot_table(china_futures, values='close', index=[china_futures.index],columns=['commodity'])
china_futures_close = china_futures_close.sort_index().fillna(method='ffill')
china_futures_close = china_futures_close['2008-01-01':'2019-10-18']

china_futures_close.to_pickle('data/china_futures_close.pkl')


china_futures_volume = china_futures[['turnover_volume', 'commodity']]

china_futures_volume = pd.pivot_table(china_futures, values='turnover_volume', index=[china_futures.index],columns=['commodity'])
china_futures_volume = china_futures_volume.sort_index().fillna(method='ffill')
china_futures_volume = china_futures_volume['2008-01-01':'2019-10-18']

china_futures_volume.to_pickle('data/china_futures_volume.pkl')