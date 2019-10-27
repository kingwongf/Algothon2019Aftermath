import pandas as pd

from tools import featGen
import matplotlib.pyplot as plt


us_eod = pd.read_pickle("data/US_EOD_20191019.pkl")
us_eod['Date'] = pd.to_datetime(us_eod.Date)
us_eod.index = us_eod.Date
us_eod = us_eod.sort_index()
us_eod = us_eod.groupby('ticker').apply(lambda x: x.fillna(method="ffill"))


us_eod['vol1m'] = us_eod.groupby('ticker')['Adj_Close'].apply(featGen.retvol, axis=0,
                                                                  args=(20,)).fillna(method='ffill')

us_eod['ret1m'] = us_eod.groupby('ticker')['Adj_Close'].apply(featGen.ret, axis=0,
                                                                  args=(20,)).fillna(method='ffill')

relevant = us_eod['2010-01-01':][['ret1m','vol1m']].resample(1000)
plt.plot(relevant)
plt.show()