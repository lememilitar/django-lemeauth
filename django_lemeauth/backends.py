from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from lemeauth import LemeAuth


class LemeAuthBackend(ModelBackend):
    """
        Authenticate using use API
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        auth = LemeAuth(username, password)
        if auth.login():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = True
                user.is_active = True
                user.save()
            return user
        return None



class AllowAllUsersLemeAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True
