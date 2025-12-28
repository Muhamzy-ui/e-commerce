import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_Jumia.settings')
import django
django.setup()
from django.contrib.auth import authenticate
print('Trying authenticate with email...')
user = authenticate(None, email='testdb@example.com', password='TestPass123')
print('authenticate(email=..):', user)
user2 = authenticate(None, username='testdb@example.com', password='TestPass123')
print('authenticate(username=..):', user2)
# show db user flags
from account.models import CustomUser
u = CustomUser.objects.filter(email='testdb@example.com').first()
print('user in DB:', u, 'is_active=', getattr(u,'is_active',None), 'is_email_verified=', getattr(u,'is_email_verified',None))
