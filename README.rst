=====
Django LemeAuth
=====

Django LemeAuth is a simple Django app to authenticate users using
Leme Auth package.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "lemeauth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'lemeauth',
    ]

2. Include the lemeauth in your  AUTHENTICATION_BACKENDS on settings.py like this:

['lemeauth.backends.LemeAuthBackend']


4. Start the development server and visit http://127.0.0.1:8000/admin/
   to athenticate with LemeAuth.
