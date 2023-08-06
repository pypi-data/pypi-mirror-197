from __future__ import print_function

import os
import socket

from flask import Flask
from micawber import bootstrap_basic
from micawber.cache import Cache as OEmbedCache
from playhouse.flask_utils import FlaskDB

from mblog.util import getUserName, getFullUserName

# Blog configuration values.
DEFAULT_HOST_IP = '0.0.0.0'
try:
    HOST = socket.gethostname() or 'localhost'
    IP = socket.gethostbyname(os.environ.get('HOST', DEFAULT_HOST_IP))
except:
    IP = DEFAULT_HOST_IP

PORT = int(os.environ.get('PORT', '5000'))
THREADS = int(os.environ.get('THREADS', '12'))

USER = getUserName()
USERNAME = getFullUserName() or USER

# You may consider using a one-way hash to generate the password, and then
# use the hash again in the login view to perform the comparison. This is just
# for simplicity.
#
# Default Password is 'Password', base64(sha2('Password')) is below.
ADMIN_PASSWORD_HASH = os.environ.get('PASSWORD_HASH', '588+9PF8OZmpTyxvYS6KiI5bECaHjk4ZOYsjvTjsIho=')

APP_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
STATIC_DIR = os.path.join(APP_DIR, 'static')

# Default: ../README.md
APP_README_FILE = os.path.join(APP_DIR, 'README.md')
if os.path.exists(APP_README_FILE):
    APP_README = open(APP_README_FILE).read()
else:
    APP_README = 'Please see README.md from the Source Code.'

# The playhouse.flask_utils.FlaskDB object accepts database URL configuration.
DATABASE_DIR = os.environ.get('DATABASE_DIR', os.path.expanduser('~'))
DATABASE = os.environ.get('DATABASE') or 'sqliteext:///%s' % os.path.join(DATABASE_DIR, '.{}-blog.db'.format(USER))
DATABASE_NEEDS_FTS = DATABASE.startswith('sqlite')

# This directory is where files are uploaded to.
UPLOAD_DIR = os.environ.get('UPLOAD_DIR') or \
             os.path.expanduser('~/.{}-blog-uploads'.format(USER))

# The secret key is used internally by Flask to encrypt session data stored
# in cookies. Make this unique for your app.
SECRET_KEY = os.environ.get('COOKIE_SECRET') or 'shhh, secret!'

# This is used by micawber, which will attempt to generate rich media
# embedded objects with maxwidth=800.
SITE_WIDTH = 400

# Debug Parameters
DEBUG = bool(os.environ.get('DEBUG', 'False'))

# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config.from_object(__name__)

# FlaskDB is a wrapper for a peewee database that sets up pre/post-request
# hooks for managing database connections.
flaskDB = FlaskDB(app)
database = flaskDB.database

# Configure micawber with the default OEmbed providers (YouTube, Flickr, etc).
# We'll use a simple in-memory cache so that multiple requests for the same
# video don't require multiple network requests.
oembedProviders = bootstrap_basic(OEmbedCache())
