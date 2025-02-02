from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import os

from user import user_bp
from administrator import administartor_bp
from transaction.view import transaction_bp
from settings import DB_CONN

app = Sanic("my_app")
app.config.SECRET_USER = os.environ.get('SECRET_USER')
app.config.SECRET_ADMINISTRATOR = os.environ.get('SECRET_ADMINISTRATOR')
app.config.SHA256_SECRET_KEY = os.environ.get('SHA256_SECRET_KEY')

bind = create_async_engine(DB_CONN, echo=True)

_sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)

_base_model_session_ctx = ContextVar("session")

@app.middleware("request")
async def inject_session(request):
    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()

app.blueprint(user_bp)
app.blueprint(administartor_bp)
app.blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12340,debug=True)