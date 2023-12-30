from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None