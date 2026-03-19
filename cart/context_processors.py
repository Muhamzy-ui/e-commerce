from .cart import Cart

def cart_count(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': len(cart)
    }
