from django.contrib.auth.models import User, Permission
from django.conf import settings

def set_default_permitions(sender, user, request, **kwargs):
    permissions = settings.LEMEAUTH_DEFAULT_PERMISSIONS
    for permission in permissions:
        p = Permission.objects.get(codename=permission)
        user.user_permissions.add(p)

    user.save()

