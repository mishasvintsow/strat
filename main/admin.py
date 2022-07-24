from django.contrib import admin
from .models import Coin, Symbol, Candle, SymbolInfo

# Register your models here.
admin.site.register(Coin)
admin.site.register(Symbol)
admin.site.register(Candle)

@admin.register(SymbolInfo)
class SymbolInfoAdmin(admin.ModelAdmin):
    list_display = ("symbol", "pnl_20_12h", "body_mean_12h", "variability", "min_diff_price",)