import jwt
from sanic import Blueprint, text, Unauthorized, Request, HTTPResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from models import User
from utils import hash_password

user_login = Blueprint("user_login", url_prefix="/login")

@user_login.post("/")
async def do_user_login(request: Request)->HTTPResponse:
    session: AsyncSession = request.ctx.session
    async with session.begin():
        email = request.json['email']
        hashed_password = hash_password(request.json['password'])
        stmt = select(User)
        stmt = stmt.where(and_(User.email==email,
                            User.hashed_password==hashed_password))
        result = await session.execute(stmt)
        person = result.scalar()

    if not person:
        raise Unauthorized()
    token = jwt.encode({"id": person.id, "email": email}, request.app.config.SECRET_USER)
    return text(token)


