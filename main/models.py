from django.db import models
import const
# Create your models here.


class Coin(models.Model):
    class Meta:
        ordering = ['coin']

    coin = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s: %s" % (self.coin, self.name)


class Symbol(models.Model):
    base = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='base') # BTC
    quote = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='quote') # USDT
    min_price = models.FloatField(default=0)
    max_price = models.FloatField(default=0)
    tick_size = models.FloatField(default=0)
    price_precision = models.IntegerField(default=0)
    qty_precision = models.IntegerField(default=0)
    min_qty = models.FloatField(default=0)
    max_qty = models.FloatField(default=0)
    step_size = models.FloatField(default=0)
    onboard_date = models.DateTimeField(null=True)
    max_leverage = models.IntegerField(default=1)
    last_update = models.DateTimeField(null=True)

    def __str__(self):
        return "%s%s" % (self.base.coin, self.quote.coin)


class SymbolInfo(models.Model):
    class Meta:
        ordering = ('-pnl_20_1h',)

    symbol = models.OneToOneField(Symbol, on_delete=models.CASCADE)
    pnl_1_max = models.FloatField(default=0)
    pnl_20_1h = models.FloatField(default=0)
    pnl_20_12h = models.FloatField(default=0)
    body_mean_1h = models.FloatField(default=0)
    body_mean_12h = models.FloatField(default=0)
    variability = models.FloatField(default=0)
    min_diff_price = models.FloatField(default=0)

    def __str__(self):
        return '%12s | PnL: %5.2f' % (str(self.symbol), self.pnl_1_max)


class Candle(models.Model):
    class Meta:
        ordering = ('symbol', 'tf', 'open_time',)

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    open = models.FloatField(null=True)
    high = models.FloatField(null=True)
    close = models.FloatField(null=True)
    low = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    tf = models.CharField(max_length=3, choices=const.KLINES_DISPLAY, default=const.KLINE_INTERVAL_1MINUTE)

    def __str__(self):
        return "[%s]%s: %s" % (self.tf, self.symbol, self.open_time)
