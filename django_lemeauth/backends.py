from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from lemeauth import LemeAuth

class LemeAuthBackend(object):
    """
        Authenticate using use API
    """

    def authenticate(self, username=None, password=None):
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


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
