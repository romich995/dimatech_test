from sanic import Blueprint, response, Request, HTTPResponse, NotFound
from sqlalchemy import select

from models import User, Account, Replenishment
from user.auth import user_protected

user_views = Blueprint("user_views", url_prefix="/")

@user_views.get('/')
@user_protected
async def get_user(request: Request, pk: int) -> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        stmt = select(User).where(User.id == pk)
        result = await session.execute(stmt)
        user = result.scalar()
    if not user:
        raise NotFound("User doesn't exist")
    return response.json(user.to_dict())


@user_views.get('/accounts')
@user_protected
async def get_accounts(request: Request, pk: int)-> HTTPResponse:
    session = request.ctx.session
    async with session.begin():
        stmt = select(User).where(User.id == pk)
        result = await session.execute(stmt)
        user = result.scalar()
        if not user:
            raise NotFound("User doesn't exist")
        stmt = select(Account).where(Account.user_id == pk)
        accounts = await session.execute(stmt)
        accounts = accounts.mappings().all()
        accounts = [{'id': account['Account'].id,
                     'balance': account['Account'].balance,
                     'user_id': account['Account'].user_id}
                    for account in accounts]
    return response.json(accounts)


@user_views.get('/replenishments')
@user_protected
async def get_replenishment(request: Request, pk: int)-> HTTPResponse:
    session = request.ctx.session
    async with (session.begin()):
        stmt = select(Replenishment)\
              .join(Replenishment.account).\
              where(Account.user_id == pk)
        replenishments = await session.scalars(stmt)
        replenishments = [{"id": replenishment.id,
                           "amount": replenishment.amount,
                           "account_id": replenishment.account_id,
                           "is_executed": replenishment.is_executed} for replenishment in replenishments]
    return response.json(replenishments)

