import pandas as pd
import numpy as np
from tools import featGen
from scipy.stats.mstats import zscore, winsorize
import swifter
from functools import reduce
pd.set_option("display.max_rows", 10000)
pd.set_option("display.max_columns", 500)



us_eod_Adj_Close = pd.read_pickle('data/us_eod_adj_close.pkl')
us_eod_Adj_Volume = pd.read_pickle('data/us_eod_adj_volume.pkl')

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

def daily_us_eod_price_feat(feat, freq, unstack=True):
    if unstack:
        return us_eod_Adj_Close.swifter.apply(feat_dict[feat], axis=0, args=(freq_dict[freq], )).fillna(method='ffill').unstack().reset_index(name=feat+freq)
    else:
        return us_eod_Adj_Close.swifter.apply(feat_dict[feat], axis=0, args=(freq_dict[freq],)).fillna(method='ffill')

mom1d = daily_us_eod_price_feat('mom','1d')
mom1w = daily_us_eod_price_feat('mom','1w')
mom1m = daily_us_eod_price_feat('mom','1m')
mom6m = daily_us_eod_price_feat('mom','6m')
mom12m = daily_us_eod_price_feat('mom','12m')

mom1m['chmom1m'] = mom1m.groupby('ticker')['mom1m'].diff(periods=1)

mom6m['chmom6m'] = mom6m.groupby('ticker')['mom6m'].diff(periods=1)
mom12m['chmom12m'] = mom12m.groupby('ticker')['mom12m'].diff(periods=1)


retvol1m = daily_us_eod_price_feat('retvol','1m')
retvol12m = daily_us_eod_price_feat('retvol','12m')
maxret1m = daily_us_eod_price_feat('maxret','1m')
maxret12m = daily_us_eod_price_feat('maxret','12m')

ema1m = daily_us_eod_price_feat('ema','1m')


RSI = us_eod_Adj_Close.apply(featGen.RSI, axis=0).fillna(method='ffill').unstack().reset_index(name='RSI')
MACD1m12m = us_eod_Adj_Close.apply(featGen.MACD, axis=0).fillna(method='ffill').unstack().reset_index(name='MACD1m12m')

return1m = us_eod_Adj_Close.pct_change(20).unstack().reset_index(name='return1m')
print(return1m)
return1m['emaret1m'] = return1m.groupby('ticker')['return1m'].rolling(20).mean()
fwd_return1m = us_eod_Adj_Close.pct_change(20).shift(-20).unstack().reset_index(name='fwd_return1m')


def mrm_c(std, vol):
    value = np.tanh((10 / vol) * 50 * std)
    value[value < -0.8] = -1
    value[value > 0.8] = 1
    value[(value >= -0.8) & (value <= 0.8)] = 0
    return value

def get_norm_side(mean, vol, ret, z ):
    side = winsorize(ret, limits = [0.025,0.025])
    side[(ret - mean)/ np.sqrt(vol) > z] = 1
    side[(ret - mean)/ np.sqrt(vol) < -z] = -1
    side[((ret - mean)/ np.sqrt(vol) >= -z) & ((ret - mean)/ np.sqrt(vol) <= z)] = 0
    return side

unstack_adj_close = us_eod_Adj_Close.unstack().reset_index(name='adj_close')

# side = fwd_return1m.apply(lambda x: get_norm_side(x.ema1m, x.retvol1m, x.fwd_return, 1.645), axis=1)
dfs = [unstack_adj_close, mom1d, mom1w, mom1m, mom6m, mom12m, retvol1m, retvol12m, maxret1m,
       maxret12m, ema1m, RSI, MACD1m12m, return1m, fwd_return1m]


name_dfs = ['ticker', 'Date', 'adj_close', 'mom1d', 'mom1w', 'mom1m', 'chmom1m', 'mom6m', 'chmom6m', 'mom12m', 'chmom12m', 'retvol1m', 'retvol12m', 'maxret1m',
       'maxret12m', 'ema1m', 'RSI', 'MACD1m12m', 'return1m', 'emaret1m', 'fwd_return1m']

unstack_df = reduce(lambda X, x: pd.merge(X, x,  how='left', left_on=['ticker','Date'], right_on = ['ticker','Date']) ,dfs)

unstack_df.columns = name_dfs
unstack_df.index = pd.to_datetime(unstack_df.Date)

unstack_df['side'] = get_norm_side(unstack_df.emaret1m, unstack_df.retvol1m, unstack_df.fwd_return1m, 1.645)

print(unstack_df[['ticker','ema1m', 'retvol1m', 'fwd_return1m','side']])
unstack_df.to_csv('data/unstack_us_eod_with_feat.csv')
