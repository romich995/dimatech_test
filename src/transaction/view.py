from sanic import Blueprint, response, Request, HTTPResponse, BadRequest
from sqlalchemy import select
from hashlib import sha256

from models import Account, Replenishment

transaction_bp = Blueprint("transaction_views", url_prefix="/transaction")

def check_signature(transaction: dict, secret_key: str):
    hsh = sha256(f"{transaction['account_id']}"
                 f"{transaction['amount']}"
                 f"{transaction['transaction_id']}"
                 f"{transaction['user_id']}"
                 f"{secret_key}".encode()).hexdigest()
    return hsh == transaction['signature']

def create_account(session, transaction):
    account = Account(id=transaction['account_id'],
            user_id=transaction['user_id'],
            balance=0)
    session.add(account)
    return account
@transaction_bp.post('/')
async def transaction(request: Request) -> HTTPResponse:
    transaction = request.json
    if check_signature(transaction, request.app.config.SHA256_SECRET_KEY):
        session = request.ctx.session
        async with session.begin():
            stmt = select(Account).where(Account.id == transaction['account_id'])
            result = await session.execute(stmt)
            account = result.scalar()
            if not account:
                account = create_account(session, transaction)

            if account.user_id != transaction['user_id']:
                raise BadRequest("Exists an account with another user")

            replenishment = Replenishment(
                id=transaction['transaction_id'],
                account_id=transaction['account_id'],
                amount=transaction['amount'])
            session.add(replenishment)
            account.balance += replenishment.amount
            return response.text("Successful")

    raise BadRequest()
