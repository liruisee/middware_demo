"""
WSGI config for solib_executor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import signal
import sys


from log_tool.log_simple_util import get_logger


logger = get_logger(app_name='manage', level='DEBUG')
project_path = os.path.abspath(__file__).rsplit('/', 2)[0]
sys.path.append(project_path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solib_executor.settings')

application = get_wsgi_application()
