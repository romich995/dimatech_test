import jwt
from sanic import Blueprint, text, Unauthorized, Request, HTTPResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from models import Administrator
from utils import hash_password

administrator_login = Blueprint("administrator_login", url_prefix="/login")
@administrator_login.post("/")
async def do_administrator_login(request: Request)->HTTPResponse:
    session: AsyncSession = request.ctx.session
    async with session.begin():
        email = request.json['email']
        hashed_password = hash_password(request.json['password'])
        stmt = select(Administrator)
        stmt = stmt.where(and_(Administrator.email==email,
                            Administrator.hashed_password==hashed_password))
        result = await session.execute(stmt)
        person = result.scalar()

    if not person:
        raise Unauthorized()
    token = jwt.encode({"id": person.id, "email": email}, request.app.config.SECRET_ADMINISTRATOR)
    return text(token)


