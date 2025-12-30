from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, default='')
    is_vendor = models.BooleanField(default=False)  # optional if you want to track vendors

    def __str__(self):
        return self.username


class VendorProfile(models.Model):
    user = models.OneToOneField('account.CustomUser', on_delete=models.CASCADE, related_name='vendor_profile')
    store_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name
