# api/content/__init__.py
from sanic import Blueprint

from .views import user_views
from .login import user_login

user_bp = Blueprint.group(user_login, user_views, url_prefix="/user")
