from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homepage.as_view(), name='homepage'),
]   