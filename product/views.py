from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from .models import Product, ProductImage, Category, Review
from .forms import ProductForm, ReviewForm
from django.db.models import Avg, Sum, Count
from orders.models import OrderItem
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    category = None
    products = Product.objects.all().order_by('-created_at').prefetch_related('reviews')

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Search by query
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    # Optional price filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Annotate with average rating
    products = products.annotate(avg_rating=Avg('reviews__rating'))

    # Latest products for sidebar
    latest_products_sidebar = Product.objects.order_by('-created_at')[:5]

    context = {
        'categories': categories,
        'category': category,
        'products': products,
        'latest_products_sidebar': latest_products_sidebar,
    }
    return render(request, 'product/product_list.html', context)


def search_live(request):
    """Return JSON search results for products and categories.

    Query param: q
    Returns: { products: [...], categories: [...] }
    """
    q = request.GET.get('q', '').strip()
    data = {'products': [], 'categories': []}
    if not q:
        return JsonResponse(data)

    # Search products
    products_qs = Product.objects.filter(name__icontains=q).order_by('-created_at')[:8]
    for p in products_qs:
        img = ''
        try:
            if p.main_image:
                img = p.main_image.url
        except Exception:
            img = ''
        data['products'].append({
            'name': p.name,
            'slug': p.slug,
            'price': str(p.price),
            'image': img,
            'type': 'product',
        })

    # Search categories
    categories_qs = Category.objects.filter(name__icontains=q)[:5]
    for c in categories_qs:
        data['categories'].append({
            'name': c.name,
            'slug': c.slug,
            'type': 'category',
        })

    return JsonResponse(data)

# -------------------------------
# Product Detail View
# -------------------------------
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.order_by('-created_at')

    # -------- Review Form --------
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product:detail', slug=slug)
    else:
        form = ReviewForm()

    # -------- Images --------
    images = []
    if product.main_image:
        images.append(product.main_image.url)
    images += [img.image.url for img in product.images.all()]

    # -------- Recently Viewed Products --------
    recently_viewed = request.session.get('recently_viewed', [])
    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)
    recently_viewed = recently_viewed[:5]
    request.session['recently_viewed'] = recently_viewed

    recently_viewed_products = Product.objects.filter(id__in=recently_viewed).exclude(id=product.id)

    # -------- "You may also like" Products --------
    # Prioritize same category, then fill with others
    same_category = list(Product.objects.filter(category=product.category).exclude(id=product.id)[:4])
    needed = 8 - len(same_category)
    other_products = list(Product.objects.exclude(id__in=[product.id] + [p.id for p in same_category]).order_by('?')[:needed])
    related_products = same_category + other_products

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'images': images,
        'recently_viewed_products': recently_viewed_products,
        'related_products': related_products,
    }
    return render(request, 'product/product_detail.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user  # <-- assign the owner
            product.save()
            # Save additional images
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            return redirect('products:detail', slug=product.slug)

    else:
        form = ProductForm()

    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'product/add_product.html', context)


def is_vendor(user):
    # Option A: treat staff users as vendors
    return user.is_authenticated and user.is_staff
    # Option B: if you have a group 'vendors': return user.groups.filter(name='vendors').exists()

# dashboard listing vendor's products
@login_required
@user_passes_test(is_vendor)
def vendor_dashboard(request):
    products = Product.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'vendor/dashboard.html', {'products': products})

# vendor add product
@login_required
@user_passes_test(is_vendor)
def vendor_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # multiple gallery images
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            for img in images:
                ProductImage.objects.create(product=product, image=img)
            return redirect('vendor:dashboard')
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'vendor/add_product.html', {'form': form, 'categories': categories})

@login_required
@user_passes_test(is_vendor)
def vendor_analytics(request):
    vendor = request.user

    # Vendor products
    products = Product.objects.filter(owner=vendor)

    total_products = products.count()

    # Order items related to vendor products
    order_items = OrderItem.objects.filter(product__owner=vendor)

    total_orders = order_items.values('order').distinct().count()

    total_revenue = order_items.aggregate(
        revenue=Sum('price')
    )['revenue'] or 0

    avg_rating = Review.objects.filter(
        product__owner=vendor
    ).aggregate(avg=Avg('rating'))['avg'] or 0

    # Top selling products
    top_products = (
        order_items
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    # Orders in last 7 days
    last_7_days = now() - timedelta(days=7)
    weekly_orders = order_items.filter(
        order__created_at__gte=last_7_days
    ).count()

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_rating': round(avg_rating, 1),
        'top_products': top_products,
        'weekly_orders': weekly_orders,
    }

    return render(request, 'vendor/analytics.html', context)