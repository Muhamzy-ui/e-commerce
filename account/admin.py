from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VendorProfile

# ---------------------------
# CustomUser Admin
# ---------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username',
        'email',
        'phone_number',
        'is_vendor',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': ('phone_number', 'is_vendor'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {
            'fields': ('phone_number', 'is_vendor'),
        }),
    )

    list_filter = UserAdmin.list_filter + ('is_vendor',)

# ---------------------------
# VendorProfile Admin
# ---------------------------
@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user_link', 'approved')
    list_filter = ('approved',)
    search_fields = ('store_name', 'user__username', 'user__email')
    actions = ['approve_vendors']

    # Make the related user clickable in the list display
    def user_link(self, obj):
        return obj.user.username
    user_link.admin_order_field = 'user'
    user_link.short_description = 'User'

    # Custom action to approve selected vendors
    def approve_vendors(self, request, queryset):
        updated = queryset.filter(approved=False).update(approved=True)
        self.message_user(request, f"{updated} vendor(s) approved successfully.")
    approve_vendors.short_description = "Approve selected vendors"
