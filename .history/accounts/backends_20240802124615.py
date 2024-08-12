from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=email ,password=None, **kwargs):
        if username is None or password is None :
            return None
        
        try:
            if '@' in username:
                user = CommonUser.objects.get(email=username)
            elif phone:
                user = CommonUser.objects.get(phone=username)
            if user.check_password(password):
                return user
        except CommonUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CommonUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
