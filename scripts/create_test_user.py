import os
import os
import sys
# Ensure project root is on sys.path
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
	sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_Jumia.settings')
import django
django.setup()
from account.models import CustomUser
print('before', CustomUser.objects.count())
CustomUser.objects.create_user(email='testdb@example.com', username='testdb', password='TestPass123', is_email_verified=True)
print('after', CustomUser.objects.count())
