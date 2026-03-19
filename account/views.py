from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, ValidationError as PasswordValidationError
from django.contrib.auth import get_user_model

from .forms import UserRegistrationForm, VendorRegistrationForm
from .models import VendorProfile, CustomUser
from orders.models import Order
from wishlist.models import Wishlist
from reviews.models import Review
from inbox.models import Message

# Use your custom user model everywhere
User = get_user_model()


# -------------------- SIGN UP --------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')  # Redirect logged-in users

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('account:register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('account:register')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return redirect('account:register')

        # Validate password strength
        try:
            validate_password(password1)
        except PasswordValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('account:register')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('account:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('account:register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully. You can now login.")
        return redirect('account:login')

    return render(request, 'account/register.html')


# -------------------- LOGIN --------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')  # Redirect logged-in users

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('products:product_list')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('account:login')

    return render(request, 'account/login.html')


# -------------------- LOGOUT --------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('account:login')


# -------------------- DASHBOARD --------------------
@login_required
def dashboard(request):
    user = request.user

    context = {
        "orders_count": Order.objects.filter(email=user.email).count(),
        "wishlist_count": Wishlist.objects.filter(user=user).count(),
        "pending_reviews_count": Review.objects.filter(
            user=user, rating__isnull=True
        ).count(),
        "unread_messages_count": Message.objects.filter(
            user=user, is_read=False
        ).count(),
        "is_vendor": False,
        "vendor_approved": False,
    }

    if user.is_vendor and hasattr(user, "vendor_profile"):
        context["is_vendor"] = True
        context["vendor_approved"] = user.vendor_profile.approved

    return render(request, "account/dashboard.html", context)



# -------------------- VENDOR REGISTRATION --------------------
def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()

            # Check if username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose another.')
                return redirect('account:register_vendor')

            # Check if email already exists
            email = form.cleaned_data['email'].strip()
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use another.')
                return redirect('account:register_vendor')

            user = form.save(commit=False)
            user.is_vendor = True
            user.save()

            # Save vendor profile
            VendorProfile.objects.create(
                user=user,
                store_name=form.cleaned_data['store_name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
            )

            messages.success(request, 'Vendor account created! Await admin approval.')
            return redirect('account:login')
    else:
        form = VendorRegistrationForm()
    return render(request, 'account/register_vendor.html', {'form': form})

# -------------------- VENDOR VERIFICATION (STAFF ONLY) --------------------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def verify_vendors(request):
    pending_vendors = VendorProfile.objects.filter(approved=False)
    return render(request, "account/verify_vendors.html", {"pending_vendors": pending_vendors})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def approve_vendor(request, vendor_id):
    vendor_profile = get_object_or_404(VendorProfile, id=vendor_id)
    
    # 1. Update Profile
    vendor_profile.approved = True
    vendor_profile.save()
    
    # 2. Update User
    user = vendor_profile.user
    user.is_vendor = True
    user.save() # Save the whole user object to be safe
    
    messages.success(request, f"Vendor {vendor_profile.store_name} has been approved successfully!")
    return redirect('account:verify_vendors')