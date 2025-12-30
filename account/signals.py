# account/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import VendorProfile
from .utils import send_vendor_approval_email


@receiver(pre_save, sender=VendorProfile)
def cache_previous_approved(sender, instance, **kwargs):
    if instance.pk:
        old = VendorProfile.objects.get(pk=instance.pk)
        instance._previous_approved = old.approved
    else:
        instance._previous_approved = False


@receiver(post_save, sender=VendorProfile)
def vendor_approved_email(sender, instance, created, **kwargs):
    # Send email ONLY when approved changes False -> True
    if not created and not instance._previous_approved and instance.approved:
        user = instance.user

        # mark user as vendor
        user.is_vendor = True
        user.save(update_fields=["is_vendor"])

        # send email safely
        if user.email:
            send_vendor_approval_email(user)
