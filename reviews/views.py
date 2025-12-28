from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import OrderItem
from .models import Review
from product.models import Product

@login_required
def pending_reviews(request):
    purchased_products = OrderItem.objects.filter(
        order__email=request.user.email
    ).values_list("product", flat=True)

    reviewed_products = Review.objects.filter(
        user=request.user
    ).values_list("product", flat=True)

    # Return Product queryset (not OrderItem) so templates can link by slug
    pending_products = Product.objects.filter(
        id__in=purchased_products
    ).exclude(
        id__in=reviewed_products
    ).exclude(
        slug__isnull=True
    ).exclude(
        slug=""
    ).distinct()

    return render(request, "reviews/pending_reviews.html", {
        "pending_products": pending_products
    })
