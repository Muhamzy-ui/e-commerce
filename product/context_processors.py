from .models import Category
from .models import Product

def categories(request):
    return {
        'all_categories': Category.objects.all(),
        'latest_products_sidebar': Product.objects.order_by('-created_at')[:6]
    }
