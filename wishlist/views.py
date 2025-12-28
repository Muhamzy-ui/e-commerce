from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from product.models import Product
from .models import Wishlist


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Prevent duplicate
    item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, "Added to wishlist ❤️")
    else:
        messages.info(request, "This product is already in your wishlist 🙂")

    # ALWAYS redirect safely
    return redirect(request.META.get("HTTP_REFERER", "wishlist:list"))


@login_required
def wishlist_page(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "wishlist/wishlist.html", {"items": items})


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Removed from wishlist ❌")

    return redirect("wishlist:list")
