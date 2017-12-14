'''
Created on Nov 11, 2017

@author: Aaron
'''
from scipy import stats
import math
import numpy as np

def ma(values, window):
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas

def ema(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()

    emas = np.convolve(values, weights, mode='full')[: len(values)]
    emas[:window] = emas[window]
    return emas

def slope(values):
    if len(values) == 0:
        return 0
    x_array = np.asarray([i+1 for i in xrange(len(values))])
    values_array = np.asarray(values)
    slope, _, _, _, _ = stats.linregress(x_array, values_array)
    return round(slope, 3)

def compound(change, window):
    """
    (1+x)^window = 1+change. e.g. (1+x)^52 = 1.6, ask x
    """
    actual = 1 + change
    x = math.pow(10, (math.log(actual, 10) / window)) - 1
    return round(x, 3) * 100

def ma_diff_ratio(values, window_1, window_2):
    """
    values is ordered by date, ascendingly
    """
    ma_1_lst = ma(values, window_1)
    ma_2_lst = ma(values, window_2)
    ma_diff = (ma_1_lst[-1] - ma_2_lst[-1]) / ma_2_lst[-1]
    return round(ma_diff, 6)

def ma_diff_trend(values, window_1, window_2, days=5):
    ma_1_lst = ma(values, window_1)
    ma_2_lst = ma(values, window_2)
    ma_diffs = []
    for i in xrange(-days, 0):
        ma_diffs.append(ma_1_lst[i]-ma_2_lst[i])
    return slope(ma_diffs)

def rsi(values, n=14):
    """
    Relative Strength Index
    """
    deltas = np.diff(values)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(values)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(values)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n
        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return round(rsi[-1], 2)
