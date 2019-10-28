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
    china_eod = pd.read_pickle("data/China_EOD_20191019.pkl")
except FileNotFoundError:
    china_eod = pd.read_csv("data/DY_SPA_f011e0f8042c364efd40ed706cf4012c.csv")
    china_eod.to_pickle("data/China_EOD_20191019.pkl")
    china_eod = pd.read_pickle("data/China_EOD_20191019.pkl")



china_eod.date = pd.to_datetime(china_eod.date)
china_eod.index = china_eod.date
china_eod = china_eod.sort_index()

china_eod_Adj_Close = china_eod[['adj_close', 'ticker']]

china_eod_Adj_Close = pd.pivot_table(china_eod, values='adj_close', index=[china_eod.index],columns=['ticker'])
china_eod_Adj_Close = china_eod_Adj_Close.sort_index().fillna(method='ffill')
china_eod_Adj_Close = china_eod_Adj_Close['2008-01-01':'2019-10-18']

china_eod_Adj_Close.to_pickle('data/china_eod_adj_close.pkl')


china_eod_Adj_Volume = china_eod[['turnover_volume', 'ticker']]

china_eod_Adj_Volume = pd.pivot_table(china_eod, values='turnover_volume', index=[china_eod.index],columns=['ticker'])
china_eod_Adj_Volume = china_eod_Adj_Volume.sort_index().fillna(method='ffill')
china_eod_Adj_Volume = china_eod_Adj_Volume['2008-01-01':'2019-10-18']

china_eod_Adj_Volume.to_pickle('data/china_eod_adj_volume.pkl')