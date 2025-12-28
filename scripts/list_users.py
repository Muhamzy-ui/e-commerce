import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_Jumia.settings')
import django
django.setup()
from account.models import CustomUser

print('All users in database:')
for u in CustomUser.objects.all():
    print(f"  Email: {u.email}")
    print(f"    Username: {u.username}")
    print(f"    is_active: {u.is_active}")
    print(f"    is_email_verified: {u.is_email_verified}")
    print()
