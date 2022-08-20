from django.urls import path

from manager import views

app_name = 'manager'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('products/<pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('categories/<pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]