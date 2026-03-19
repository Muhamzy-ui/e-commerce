from django import template
from cart.cart import Cart

register = template.Library()

@register.filter
def cart_quantity(product_id, request):
    """
    Returns the quantity of a product in the cart.
    Usage: {{ product.id|cart_extras:request }}
    """
    cart = Cart(request)
    product_id = str(product_id)
    if product_id in cart.cart:
        return cart.cart[product_id]['quantity']
    return 0
