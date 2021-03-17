from django.urls import path, include
from .views import *

urlpatterns = [  
   path('list/', UserListView.as_view(), name='user_list'),
   path('add/', UserRegisterView.as_view(), name='user_add'),
   path('update/<pk>/', UserUpdateView.as_view(), name='user_update'),
   path('resetpass/', UpdatePasswordView.as_view(), name='user_p_update'),
   path('del/<pk>/', UsuarioDel.as_view(), name='user_del'),
]