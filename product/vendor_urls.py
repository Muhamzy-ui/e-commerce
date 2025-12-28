# product/vendor_urls.py
from django.urls import path
from . import views

app_name = 'vendor'

urlpatterns = [
    path('', views.vendor_dashboard, name='dashboard'),
    path('add/', views.vendor_add_product, name='add_product'),
    path("analytics/", views.vendor_analytics, name="analytics"),
]
