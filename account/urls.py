from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('verify-vendors/', views.verify_vendors, name='verify_vendors'),
    path('approve-vendor/<int:vendor_id>/', views.approve_vendor, name='approve_vendor'),
]
