from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('process_pedido/', process_pedido, name='process_pedido'),
    path('me/', login_required(peididoList.as_view(), login_url='bases:login'), name='peididoList'),
    path('<int:pk>', login_required(pedidoDetail.as_view(), login_url='bases:login'), name='pedidoDetail'),
]
