from django.contrib import admin
from .models import Coin, Symbol, Candle

# Register your models here.
admin.site.register(Coin)
admin.site.register(Symbol)
admin.site.register(Candle)
