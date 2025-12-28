from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("checkout/", views.checkout_page, name="checkout"),
    path("process/", views.process_checkout, name="process_checkout"),
    path("bank-transfer/<str:reference>/", views.bank_transfer_page, name="bank_transfer"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
]
