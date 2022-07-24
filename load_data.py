from datetime import timedelta

import binance
import pandas as pd
from django.utils import timezone

from connect import connect
from main.models import Coin, Symbol, Candle
import const
from django.core.exceptions import ObjectDoesNotExist


# datetime.datetime(2022, 6, 14, 14, 15)


def get_candles(client, symbol, start_time, end_time, tf):
    # start_time_ms = timezone.make_aware(start_time).strftime("%d %b, %Y %H:%M")
    # end_time_ms = timezone.make_aware(end_time).strftime("%d %b, %Y %H:%M")
    start_time_ms = start_time.strftime("%d %b, %Y %H:%M")
    end_time_ms = end_time.strftime("%d %b, %Y %H:%M")

    candles = client.futures_historical_klines(symbol,
                                               tf,
                                               start_str=start_time_ms,
                                               end_str=end_time_ms)

    df = pd.DataFrame(candles,
                      columns=['datetime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume',
                               'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms').dt.strftime("%m/%d/%Y, %H:%M:%S")
    df.set_index('datetime', inplace=True)

    df = df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'],
                 axis=1)
    df.index = pd.DatetimeIndex(df.index)
    df['open'] = df['open'].apply(lambda x: float(x))
    df['high'] = df['high'].apply(lambda x: float(x))
    df['low'] = df['low'].apply(lambda x: float(x))
    df['close'] = df['close'].apply(lambda x: float(x))
    df['volume'] = df['volume'].apply(lambda x: float(x))
    return df


def get_coins_info(client):
    # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.get_all_coins_info
    return [{'coin': c['coin'], 'name': c['name']} for c in client.get_all_coins_info()]


def get_symbols_info(client, symbol=None):
    info = client.futures_exchange_info()['symbols']
    if symbol is None:
        return info
    else:
        return [c for c in info if c['symbol'] == "BTCUSDT"][0]


def fill_db_coins(client):
    coins = get_coins_info(client)
    for coin in coins:
        Coin.objects.get_or_create(coin=coin['coin'], defaults={'name': coin['name']})


def fill_db_symbols(client):
    info = pd.DataFrame(get_symbols_info(client))
    info = info[info['contractType'] == 'PERPETUAL']
    info = info[info['status'] == 'TRADING']
    info = info[info['symbol'].str.contains('USDT')]
    info['minPrice'] = info['filters'].apply(lambda x: x[0]['minPrice'])
    info['maxPrice'] = info['filters'].apply(lambda x: x[0]['maxPrice'])
    info['tickSize'] = info['filters'].apply(lambda x: x[0]['tickSize'])
    info['stepSize'] = info['filters'].apply(lambda x: x[1]['stepSize'])
    info['minQty'] = info['filters'].apply(lambda x: x[1]['minQty'])
    info['maxQty'] = info['filters'].apply(lambda x: x[1]['maxQty'])
    info['onboardDate'] = pd.to_datetime(info['onboardDate'], unit='ms')
    info.drop(columns=['contractType', 'deliveryDate', 'pair',
                       'status', 'requiredMarginPercent', 'quoteAsset',
                       'maintMarginPercent', 'underlyingType', 'underlyingSubType',
                       'settlePlan', 'triggerProtect', 'liquidationFee',
                       'marketTakeBound', 'timeInForce', 'orderTypes', 'filters',
                       'baseAssetPrecision', 'quotePrecision'], inplace=True)
    for symbol in info.to_dict('records'):
        Symbol.objects.update_or_create(base=Coin.objects.get_or_create(coin=symbol['baseAsset'])[0],
                                     quote=Coin.objects.get(coin='USDT'),
                                     defaults={'price_precision': symbol['pricePrecision'],
                                               'qty_precision': symbol['quantityPrecision'],
                                               'min_price': symbol['minPrice'],
                                               'max_price': symbol['maxPrice'],
                                               'min_qty': symbol['minQty'],
                                               'tick_size': symbol['tickSize'],
                                               'step_size': symbol['stepSize'],
                                               'onboard_date': timezone.make_aware(symbol['onboardDate'])})


def update_symbol_klines(client, symbol, start_date, end_date):
    try:
        client.ping()
    except binance.BinanceAPIException:
        client = connect()
    symbol.last_update = timezone.now()
    symbol.save()
    data = get_candles(client, str(symbol), start_date, end_date, const.KLINE_INTERVAL_5MINUTE)
    data['date'] = data.index
    for row in data.to_dict('records'):
        Candle.objects.update_or_create(symbol=symbol, open_time=timezone.make_aware(row['date']),
                                        tf=const.KLINE_INTERVAL_5MINUTE,
                                        defaults={'close_time': timezone.make_aware(row['date'] + timedelta(minutes=5)),
                                                  'open': row['open'],
                                                  'high': row['high'],
                                                  'low': row['low'],
                                                  'close': row['close'],
                                                  'volume': row['volume'],
                                                  })
    return data


def update_klines_day():
    client = connect()
    for symbol in Symbol.objects.all():
        try:
            client.ping()
        except binance.BinanceAPIException:
            client = connect()
        update_symbol_klines(client, symbol, timezone.now() - timedelta(minutes=1450), timezone.now())
    return True


def update_klines_missed():
    client = connect()
    for symbol in Symbol.objects.all():
        try:
            client.ping()
        except binance.BinanceAPIException:
            client = connect()
        update_symbol_klines(client,
                             symbol,
                             Candle.objects.filter(symbol=symbol).last().open_time-timedelta(minutes=10),
                             timezone.now())


def update_leverages(client):
    lev_info = [c for c in client.futures_leverage_bracket() if 'USDT' in c['symbol']]
    for L in lev_info:
        try:
            symbol = Symbol.objects.get(base__coin=L['symbol'].replace("USDT", ''))
        except ObjectDoesNotExist:
            continue
        symbol.max_leverage = max([b['initialLeverage'] for b in L['brackets']])
        symbol.save()
