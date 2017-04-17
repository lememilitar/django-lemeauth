import pytest
import os
import unittest

from django.test import TestCase
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.module_loading import import_string
from django_lemeauth.backends import LemeAuthBackend



def credentials():
    return (os.getenv('USER'), os.getenv('PASS'))

@pytest.mark.django_db
class TestAuthBackend(TestCase):
    def test_authenticate_user(self):
        username, password = credentials()
        user = authenticate(username=username, password=password)
        self.assertEqual(user.username, username)
        self.assertEqual(user.is_superadmin, True)


    def test_not_authenticate_user(self):
        username, password = credentials()
        password = 'test'
        self.assertRaises(PermissionDenied, authenticate(username=username, password=password))

    def test_load_backend(self):
        for backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = import_string(backend_path)()
            self.assertIsInstance(backend, LemeAuthBackend)

    def test_login_no_superadmin(self):
        settings.LEMEAUTH_SUPERADMINS = []
        username, password = credentials()
        user = authenticate(username=username, password=password)
        self.assertEqual(user.username, username)
        self.assertEqual(user.is_superadmin, False)


    def test_default_permitions_is_setted_after_login(self):
        username, password = credentials()
        user = authenticate(username=username, password=password)
        self.assertTrue(user.has_perm('auth.change_user'))
