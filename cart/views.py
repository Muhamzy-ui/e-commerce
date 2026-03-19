from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from .cart import Cart

def cart_page(request):
    cart = Cart(request)
    cart_items = list(cart)  # list of items
    total_price = cart.get_total_price()

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "cart/cart.html", context)

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def adjust_cart(request, product_id, action):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if action == 'increase':
        cart.add(product)
    elif action == 'decrease':
        cart.decrease(product)
    return redirect('cart:cart_page')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_page')
