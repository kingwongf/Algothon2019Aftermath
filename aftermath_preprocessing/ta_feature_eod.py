import pandas as pd
import numpy as np
from tools import featGen
from scipy.stats.mstats import zscore, winsorize
import swifter
pd.set_option("display.max_rows", 10000)
pd.set_option("display.max_columns", 500)

us_eod = pd.read_pickle('data/filtered_us_eod.pkl')

us_eod['Date'] = pd.to_datetime(us_eod.Date)
us_eod.index = us_eod.Date
us_eod = us_eod.sort_index()
us_eod = us_eod.groupby('ticker').apply(lambda x: x.fillna(method="ffill"))

## TODO sample


feat_dict = {'mom': featGen.momentum,
             'retvol': featGen.retvol,
             'ema': featGen.ema,
             'RSI': featGen.RSI,
             'MACD': featGen.MACD,
             'maxret': featGen.maxret
             }
freq_dict = {'1d': 1,
             '1w': 5,
             '1m': 20,
             '6m': 125,
             '12m': 250
             }

def daily_us_eod_price_feat(feat, freq):
    us_eod[feat + freq] = us_eod.groupby('ticker')['Adj_Close'].apply(feat_dict[feat], axis=0, args=(freq_dict[freq], )).fillna(method='ffill')


daily_us_eod_price_feat('mom','1d')
daily_us_eod_price_feat('mom','1w')
daily_us_eod_price_feat('mom','1m')
daily_us_eod_price_feat('mom','6m')
daily_us_eod_price_feat('mom','12m')
us_eod['chmom1m'] = us_eod.groupby('ticker')['mom1m'].apply(np.diff(periods=1))
us_eod['chmom6m'] = us_eod.groupby('ticker')['mom6m'].apply(np.diff(periods=1))
us_eod['chmom12m'] = us_eod.groupby('ticker')['mom12m'].apply(np.diff(periods=1))

daily_us_eod_price_feat('retvol','1m')
daily_us_eod_price_feat('retvol','12m')
daily_us_eod_price_feat('maxret','1m')
daily_us_eod_price_feat('maxret','12m')

daily_us_eod_price_feat('ema','1m')


us_eod['RSI'] = us_eod.groupby('ticker')['Adj_Close'].apply(featGen.RSI, axis=0).fillna(method='ffill')
us_eod['MACD1m12m'] = us_eod.groupby('ticker')['Adj_Close'].apply(featGen.MACD, axis=0).fillna(method='ffill')

us_eod['adj_dollar_vol'] = us_eod['Adj_Volume'] * us_eod['Adj_Close']


us_eod["return"] = us_eod.groupby("ticker")["Adj_Close"].pct_change(20)
us_eod["fwd_return"] = us_eod.groupby("ticker")["return"].shift(-20)


def mrm_c(std, vol):
    value = np.tanh((10 / vol) * 50 * std)
    value[value < -0.8] = -1
    value[value > 0.8] = 1
    value[(value >= -0.8) & (value <= 0.8)] = 0
    return value

def get_norm_side(mean,vol, ret,z ):
    side = winsorize(ret, limits = [0.025,0.025])
    side[(ret - mean)/ np.sqrt(vol) > z] = 1
    side[(ret - mean)/ np.sqrt(vol) < -z] = -1
    side[((ret - mean)/ np.sqrt(vol) >= z) & ((ret - mean)/ np.sqrt(vol) <= z)] = 0
    return side


us_eod['side'] = us_eod.groupby("ticker")["fwd_return"].apply(lambda x: get_norm_side(x.ema1m, x.retvol1m, x.fwd_return, 1.645), axis=1)

print(us_eod.head(1000))

us_eod.to_pickle('data/feat_US_EOD_20191019.pkl')