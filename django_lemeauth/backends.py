from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Permission
from django.conf import settings
from lemeauth import LemeAuth

class LemeAuthBackend(ModelBackend):
    """
        Authenticate using the API
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = username.lower()
        auth = LemeAuth(username, password)
        if auth.login():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = True
                user.is_active = True
                user.is_superuser = self.is_superuser(user)
                user.save()
                self.set_default_permissions(user)
            return user
        return None


    def is_superuser(self, user):
        included = user.username in settings.LEMEAUTH_SUPERADMINS
        return included

    def set_default_permissions(self, user):
        permissions = settings.LEMEAUTH_DEFAULT_PERMISSIONS
        for permission in permissions:
            p = Permission.objects.get(codename=permission)
            user.user_permissions.add(p)

        user.save()


class AllowAllUsersLemeAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return True
