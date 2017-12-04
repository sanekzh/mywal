from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

__all__ = ['celery_app']


from mywal.settings import *

try:
    from mywal.local_settings import *
except ImportError:
    from mywal.settings import *
