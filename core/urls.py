from django.urls import path

from core import views
from django.contrib.auth.views import logout_then_login

app_name = 'core'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),

    path('', views.ProductListView.as_view(), name='product-list'),
    path('product/<pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]