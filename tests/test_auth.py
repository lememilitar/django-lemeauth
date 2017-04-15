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
        print(username, password)
        user = authenticate(username=username, password=password)
        self.assertEqual(user.username, username)


    def test_not_authenticate_user(self):
        username, password = credentials()
        password = 'test'
        self.assertRaises(PermissionDenied, authenticate(username=username, password=password))

    def test_load_backend(self):
        for backend_path in settings.AUTHENTICATION_BACKENDS:
            backend = import_string(backend_path)()
            self.assertIsInstance(backend, LemeAuthBackend)
