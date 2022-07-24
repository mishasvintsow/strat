import numpy as np
import pandas as pd

from main.models import Candle, SymbolInfo

fee = 4e-4


def pnl(current_price, diff_price, init_volume):
    return init_volume*(1-fee)*diff_price/current_price - 2*init_volume*fee


def update_minute(symbol):
    klines = Candle.objects.filter(symbol=symbol).order_by('-open_time')[:13]
    data = pd.DataFrame(klines.values('open', 'high', 'low', 'close')[1:])
    data['body'] = np.abs(data['open']-data['close'])
    current_price = (klines.first().open+klines.first().close)/2
    body_mean_1h = data['body'].mean()
    pnl_1_max = pnl(current_price, body_mean_1h, symbol.max_leverage)
    pnl_20_1h = pnl(current_price, body_mean_1h, 20)
    min_diff_price = 2*current_price*fee/(1-fee)
    SymbolInfo.objects.update_or_create(symbol=symbol,
                                        defaults={'pnl_1_max': pnl_1_max,
                                                  'pnl_20_1h': pnl_20_1h,
                                                  'body_mean_1h': body_mean_1h,
                                                  'min_diff_price': min_diff_price})
    return True


def update_5minutes(symbol):
    klines = Candle.objects.filter(symbol=symbol).order_by('-open_time')[:145]
    data = pd.DataFrame(klines.values('open', 'high', 'low', 'close'))
    var_5m_sum = np.sum((2*(data['high']-data['low'])-np.abs(data['open']-data['close']))/data['low']*100)
    data['body'] = np.abs(data['open']-data['close'])
    body_mean_12h = data['body'].mean()
    current_price = (klines.first().open+klines.first().close)/2
    pnl_20_12h = pnl(current_price, body_mean_12h, 20)
    SymbolInfo.objects.update_or_create(symbol=symbol,
                                        defaults={'variability': var_5m_sum,
                                                  'pnl_20_12h': pnl_20_12h,
                                                  'body_mean_12h': body_mean_12h})
    return True


