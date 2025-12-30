from django.core.mail import send_mail
from django.conf import settings


def send_vendor_approval_email(user):
    subject = "Your Vendor Account Has Been Approved 🎉"
    message = f"""
Hello {user.username},

Congratulations 🎉

Your vendor account has been approved.
You can now start uploading products and selling on My Jumia.

Best regards,
My Jumia Team
"""

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log error instead of crashing admin
        print("EMAIL ERROR:", e)
