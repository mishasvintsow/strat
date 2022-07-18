from django.urls import path, re_path
from main import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('coins', views.CoinsListView.as_view(), name='coins'),
    path('futures', views.FuturesListView.as_view(), name='futures'),
    path('futures/info', views.FuturesInfoListView.as_view(), name='futures_info'),
]
