from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order 
from wishlist.models import Wishlist
from reviews.models import Review
from inbox.models import Message

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def dashboard(request):
    context = {
        "orders_count": Order.objects.filter(email=request.user.email).count(),
        "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
        "pending_reviews_count": Review.objects.filter(user=request.user, rating__isnull=True).count(),
        "unread_messages_count": Message.objects.filter(user=request.user, is_read=False).count(),
    }
    return render(request, "account/dashboard.html", context)