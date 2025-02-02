from sanic import Blueprint, response, Request, HTTPResponse, NotFound
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models import Administrator, User
from administrator.auth import administrator_protected
from utils import hash_password

administrator_views = Blueprint("administrator_views", url_prefix="/")


@administrator_views.get('/')
@administrator_protected
async def get_administrator(request: Request, pk: int) -> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        stmt = select(Administrator).where(Administrator.id == pk)
        result = await session.execute(stmt)
        user = result.scalar()
    if not user:
        raise NotFound("Administrator doesn't exist")
    return response.json({"id": user.id,
                          "email": user.email,
                          "full_name": user.full_name
                          })


@administrator_views.post('/user')
@administrator_protected
async def create_user(request: Request, pk: int) -> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        user = User(email=request.json['email'],
                 full_name=request.json['full_name'],
                 hashed_password=hash_password(request.json['password']))
        session.add_all([user])

    return response.json(user.to_dict())

@administrator_views.delete('/user')
@administrator_protected
async def delete_user(request: Request, pk: int) -> HTTPResponse:
    session: AsyncSession = request.ctx.session
    async with session.begin():
        stmt = select(User).where(User.id == request.json['id'])
        result = await session.execute(stmt)
        user = result.scalar()
        await session.delete(user)
    return response.text('Deleted')


@administrator_views.patch('/user')
@administrator_protected
async def update_user(request: Request, pk: int) -> HTTPResponse:
    session = request.ctx.session
    data = request.json
    async with session.begin():
        stmt = select(User).where(User.id == request.json['id'])
        result = await session.execute(stmt)
        user = result.scalar()
        if 'email' in data:
            user.email = data['email']
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'password' in data:
            user.hashed_password = hash_password(data['password'])

    return (response.json(user.to_dict()))


@administrator_views.get('/users/')
@administrator_protected
async def get_user(request: Request, pk: int) -> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        stmt = select(User).options(selectinload(User.accounts))
        result = await session.execute(stmt)
        users = result.scalars()
        data = [{**user.to_dict(), "accounts": [ account.to_dict() for account in user.accounts]} for user in users]
        return response.json(data)


