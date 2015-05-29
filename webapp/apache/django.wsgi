# vim: set ft=python:

import os, sys
sys.path.append("/usr/local/videoserver")
sys.path.append("/usr/local/videoserver/library")
os.environ["DJANGO_SETTINGS_MODULE"] = "library.settings"
os.environ["PYTHON_EGG_CACHE"] = "/usr/local/videoserver/library/egg-cache"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

