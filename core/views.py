from django.shortcuts import render
from product.models import Category, Product

def home(request):
    categories = Category.objects.all()

    latest_products = Product.objects.order_by("-created_at")[:8]
    sales_products = Product.objects.filter(is_flash_sale=True)[:8]
    recommended = Product.objects.order_by("?")[:8]

    return render(request, "home.html", {
        "categories": categories,
        "latest_products": latest_products,
        "sales_products": sales_products,
        "recommended": recommended,
    })
