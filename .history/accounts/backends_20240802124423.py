from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=email ,password=None, **kwargs):
        if email is None or password is None or phone is None:
            return None
        
        try:
            if email:
                user = User.objects.get(email=email)
            elif phone:
                user = User.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
