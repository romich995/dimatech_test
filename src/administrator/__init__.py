from sanic import Blueprint

from .views import administrator_views
from .login import administrator_login

administartor_bp = Blueprint.group(administrator_login, administrator_views, url_prefix="/administrator")