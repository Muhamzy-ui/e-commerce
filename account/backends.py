from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailBackend(ModelBackend):
    """Authenticate using email instead of username."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f'EmailBackend.authenticate() called with username={username}')
        try:
            user = CustomUser.objects.get(email=username)
            print(f'EmailBackend: found user {user.email}')
        except CustomUser.DoesNotExist:
            print(f'EmailBackend: no user found with email {username}')
            return None
        
        pwd_valid = user.check_password(password)
        print(f'EmailBackend: password valid={pwd_valid}')
        
        can_auth = self.user_can_authenticate(user)
        print(f'EmailBackend: user_can_authenticate={can_auth} (is_active={user.is_active})')
        
        if pwd_valid and can_auth:
            print(f'EmailBackend: returning user {user.email}')
            return user
        
        print(f'EmailBackend: authentication failed')
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
