from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('adjust/<int:product_id>/<str:action>/', views.adjust_cart, name='adjust_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
