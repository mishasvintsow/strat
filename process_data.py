import numpy as np
import pandas as pd

from main.models import Candle, SymbolInfo

fee = 4e-4


def pnl(current_price, diff_price, init_volume):
    return init_volume*(1-fee)*diff_price/current_price - 2*init_volume*fee


def update_pnl(symbol):
    klines = Candle.objects.filter(symbol=symbol).order_by('-open_time')[:13]
    data = pd.DataFrame(klines.values('open', 'high', 'low', 'close')[1:])
    data['body'] = np.abs(data['open']-data['close'])
    current_price = (klines.first().open+klines.first().close)/2
    body_mean = data['body'].mean()
    pnl_1max = pnl(current_price, body_mean, symbol.max_leverage)
    pnl_20 = pnl(current_price, body_mean, 20)
    SymbolInfo.objects.update_or_create(symbol=symbol,
                                        defaults={'pnl_1_max': pnl_1max,
                                                  'pnl_20': pnl_20,
                                                  'body_mean': body_mean})
    return pnl_1max

