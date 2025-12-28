import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_Jumia.settings')
import django
django.setup()
from django.contrib.auth import authenticate
from account.backends import EmailBackend
from account.models import CustomUser

# Test the backend directly
backend = EmailBackend()
print('Testing EmailBackend directly...')
user = backend.authenticate(None, username='testdb@example.com', password='TestPass123')
print('EmailBackend.authenticate():', user)

# Test via Django's authenticate()
print('\nTesting via Django authenticate()...')
user2 = authenticate(None, username='testdb@example.com', password='TestPass123')
print('authenticate():', user2)

# Check what's in DB
print('\nUsers in DB:')
for u in CustomUser.objects.all():
    print(f"  {u.email} (id={u.id}, is_active={u.is_active}, is_email_verified={u.is_email_verified})")
