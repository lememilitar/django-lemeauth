from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from lemeauth import LemeAuth


UserModel = get_user_model()

class LemeAuthBackend(ModelBackend):
    """
        Authenticate using use API
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        auth = LemeAuth(username, password)
        if auth.login():
            try:
                user = User.objects.get(username=username)
            except:
                user = User(username=username)
                user.is_staff = True
                user.is_active = True
                user.save()
            return user
        return None
