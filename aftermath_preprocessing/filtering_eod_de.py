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
    us_eod = pd.read_pickle("data/US_EOD_20191019.pkl")
except FileNotFoundError:
    us_eod = pd.read_csv("data/US_EOD_20191019.csv", names=['ticker','Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividend', 'Split'
                                                               ,'Adj_Open', 'Adj_High', 'Adj_Low', 'Adj_Close', 'Adj_Volume'])
    us_eod.to_pickle("data/US_EOD_20191019.pkl")
    us_eod = pd.read_pickle("data/US_EOD_20191019.pkl")

li = pd.read_csv('data/overlapping_companies.txt')
overlapping_tickers = li.columns.tolist()
us_eod = us_eod[us_eod['ticker'].isin(overlapping_tickers)]

us_eod.to_pickle('data/filtered_us_eod.pkl')
exit()
