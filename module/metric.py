'''
Created on Nov 11, 2017

@author: Aaron
'''
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

def ma_diff_ratio(values, window_1, window_2):
    """
    values is ordered by date, ascendingly
    """
    ma_1_lst = ma(values, window_1)
    ma_2_lst = ma(values, window_2)
    ma_diff = (ma_1_lst[-1] - ma_2_lst[-1]) / ma_2_lst[-1]
    return round(ma_diff, 6) 

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
