'''
Created on Nov 11, 2017

@author: Aaron
'''
from scipy import stats
import math
import numpy as np

def ma(values, window):
    if window > len(values):
        return np.asarray(values)
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

class MADIFF(object):
    def __init__(self, vals, wd1, wd2):
        """
            values is ordered by date, ascendingly
        """
        self.values = vals
        self.ma_1_lst = ma(vals, wd1)
        self.ma_2_lst = ma(vals, wd2)

    def ratio(self, idx=-1):
        ma_diff = (self.ma_1_lst[idx] - self.ma_2_lst[idx]) / \
                    self.ma_2_lst[idx]
        return round(ma_diff, 4)

    def trend(self, duration=10):
        if len(self.ma_1_lst) < duration or \
                len(self.ma_2_lst) < duration:
            return -100
        ma_diffs = []
        for i in xrange(-duration, 0):
            ma_diffs.append(self.ma_1_lst[i]-self.ma_2_lst[i])
        return slope(ma_diffs)

    def rally_days(self):
        min_len = len(self.ma_1_lst) >= len(self.ma_2_lst) and \
                len(self.ma_2_lst) or len(self.ma_1_lst) 
        
        i = -1
        days = 0
        start_idx = -min_len
        while i >= start_idx:
            ma_diff = (self.ma_1_lst[i] - self.ma_2_lst[i]) / \
                    self.ma_2_lst[i]
            if ma_diff <= 0:
                break
            i -= 1
            days += 1
        return days

    def rally_gain(self):
        days = self.rally_days()
        price_start = self.values[-days]
        price_now = self.values[-1]
        price_change = (price_now-price_start) / price_start
        return round(price_change, 4)

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
