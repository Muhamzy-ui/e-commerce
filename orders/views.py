import uuid
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required

PAYSTACK_INITIALIZE = "https://api.paystack.co/transaction/initialize"
PAYSTACK_VERIFY = "https://api.paystack.co/transaction/verify/"

@login_required(login_url='account:login')
def checkout_page(request):
    cart = Cart(request)
    if len(cart) == 0:
        return render(request, "orders/empty_cart.html")
    form = CheckoutForm()
    return render(request, "orders/checkout.html", {"cart": cart, "cart_total": cart.get_total_price(), "form": form})

@login_required(login_url='account:login')
def process_checkout(request):
    if request.method != "POST":
        return redirect("orders:checkout")
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("home")

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        return render(request, "orders/checkout.html", {"cart": cart, "cart_total": cart.get_total_price(), "form": form})

    cd = form.cleaned_data
    payment_method = cd["payment_method"]
    order_number = str(uuid.uuid4()).replace("-", "")[:12]

    order = Order.objects.create(
        order_number=order_number,
        full_name=cd["full_name"],
        email=cd["email"],
        phone=cd["phone"],
        address=cd["address"],
        state=cd["state"],
        payment_method=payment_method,
        total=cart.get_total_price(),
    )

    for item in cart:
        OrderItem.objects.create(order=order, product=item["product"], price=item["price"], quantity=item["quantity"])

    if payment_method == "bank":
        cart.clear()
        return render(request, "orders/bank_transfer.html", {
            "order": order, "bank_name": "GTBank", "account_name": "MZCart Marketplace", "account_number": "1028627906", "amount": order.total,
        })

    if payment_method == "paystack":
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}", "Content-Type": "application/json"}
        data = {"email": order.email, "amount": int(order.total * 100), "reference": order.order_number, "callback_url": request.build_absolute_uri(reverse("orders:payment_success"))}
        resp = requests.post(PAYSTACK_INITIALIZE, json=data, headers=headers, timeout=30)
        try:
            resp_json = resp.json()
        except Exception:
            return redirect("orders:payment_failed")
        if resp.status_code in (200,201) and resp_json.get("status"):
            cart.clear()
            return redirect(resp_json["data"]["authorization_url"])
        return redirect("orders:payment_failed")

    if payment_method == "pod":
        cart.clear()
        return render(request, "orders/pay_on_delivery.html", {"order": order})

    return redirect("cart:cart_page")

@login_required(login_url='account:login')
@csrf_exempt
def payment_success(request):
    reference = request.GET.get("reference") or request.POST.get("reference")
    if not reference:
        return render(request, "orders/payment_failed.html")

    verify_url = PAYSTACK_VERIFY + reference
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    try:
        resp = requests.get(verify_url, headers=headers, timeout=30)
        resp_json = resp.json()
    except Exception as e:
        return render(request, "orders/payment_failed.html", {"error": str(e)})

    if resp.status_code == 200 and resp_json.get("data", {}).get("status") == "success":
        order_number = resp_json["data"]["reference"]
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return render(request, "orders/payment_failed.html", {"error": "Order not found"})

        order.status = "paid"
        order.payment_reference = reference
        order.payment_date = timezone.now()
        order.save()

        # send email
        try:
            send_mail("Payment Successful - MZCart",
                      f"Your order {order.order_number} has been paid successfully!",
                      settings.EMAIL_HOST_USER,
                      [order.email],
                      fail_silently=True)
        except Exception:
            pass

        # optional: send SMS via TERMII (requires TERMII_API_KEY in settings)
        try:
            sms_url = "https://api.ng.termii.com/api/sms/send"
            sms_data = {"api_key": settings.TERMII_API_KEY, "to": order.phone, "from": "MZCart", "sms": f"Payment received for Order {order.order_number}. Thank you!", "type": "plain", "channel": "generic"}
            requests.post(sms_url, json=sms_data, timeout=10)
        except Exception:
            pass

        return render(request, "orders/payment_success.html", {"order": order})

    return render(request, "orders/payment_failed.html")

def bank_transfer_page(request, reference):
    order = get_object_or_404(Order, order_number=reference)
    return render(request, "orders/bank_transfer.html", {"order": order})

def payment_failed(request):
    return render(request, "orders/payment_failed.html")

@login_required
def order_list(request):
    orders = Order.objects.filter(
        email=request.user.email
    ).order_by("-created_at")

    return render(request, "orders/order_list.html", {
        "orders": orders
    })