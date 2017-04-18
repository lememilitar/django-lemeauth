from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Permission
from django.conf import settings
from lemeauth import LemeAuth


class LemeAuthBackend(ModelBackend):
    """
        Authenticate using use API
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        username = username.lower()
        auth = LemeAuth(username, password)
        if auth.login():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = True
                user.is_active = True
                user.is_superadmin = self.is_superadmin(user)
                user.save()
                self.set_default_permitions(user)
            return user
        return None


    def is_superadmin(self, user):
        return user.username in settings.LEMEAUTH_SUPERADMINS


    def set_default_permitions(self, user):
        permissions = settings.LEMEAUTH_DEFAULT_PERMISSIONS
        for permission in permissions:
            p = Permission.objects.get(codename=permission)
            user.user_permissions.add(p)

        user.save()



class AllowAllUsersLemeAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True
