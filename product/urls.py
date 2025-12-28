from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search-live/', views.search_live, name='search_live'),
     path('add/', views.add_product, name='add_product'),
    path('category/<slug:category_slug>/', views.product_list, name='category'),  
    path('<slug:slug>/', views.product_detail, name='detail'),
]
