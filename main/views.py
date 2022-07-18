from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from main.models import Coin, Symbol, SymbolInfo


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'Start Page'
        return context


class CoinsListView(ListView):
    model = Coin
    context_object_name = 'coins'
    template_name = 'main/coins.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'Coins'
        return context


class FuturesListView(ListView):
    model = Symbol
    context_object_name = 'symbols'
    template_name = 'main/futures.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'Futures'
        return context


class FuturesInfoListView(ListView):
    model = SymbolInfo
    context_object_name = 'symbolinfos'
    template_name = 'main/futures_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'Futures Info'
        return context
