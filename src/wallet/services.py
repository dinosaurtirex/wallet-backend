from sanic import Request 
from sanic.response import HTTPResponse
from sanic.response import json 

from utils.settings import API_CODES
from wallet.models import Balance
from auth.models import User


class BalanceService:

    def process_currency(self, currency: str) -> None:
        if len(currency) > 5:
            raise ValueError(API_CODES[1005])
        return currency

    def process_tag(self, tag: str) -> str:
        return tag.lstrip().rstrip().replace(" ","_").lower()

    async def get_current_balance(self, owner: User, currency: str) -> float:
        if currency is None:
            raise ValueError(API_CODES[1006])
        balance_instances = await Balance.filter(
            owner=owner, 
            currency=currency
        )
        if len(balance_instances) == 0:
            return 0.0
        return balance_instances[-1].amount

    async def insert_or_spent_money(
        self, 
        insert: bool, 
        currency: str, 
        amount: float, 
        tag: str | None, 
        description: str | None, 
        owner: User
    ) -> Balance:
        current_amount = await self.get_current_balance(owner, currency)
        if insert:
            new_amount = current_amount + amount 
        else:
            new_amount = current_amount - amount 
            if new_amount < 0:
                raise ValueError(API_CODES[1007])
        return await Balance.create(
            currency=currency,
            amount=new_amount,
            tag=tag,
            description=description,
            owner=owner
        )
    
    async def get_transaction_history(
        self, 
        currency: str, 
        owner: User
    ) -> list[Balance]:
        arguments = {
            "owner":    owner,
            "currency": currency
        }
        transactions = await Balance.filter(**arguments)
        history = []
        for i, transaction in enumerate(transactions):
            if i == 0:
                history.append({
                    "diffrence": transaction.amount ,
                    "datetime": str(transaction.added_at),
                    "currency": transaction.currency
                })
            else:
                history.append({
                    "diffrence": transaction.amount - transactions[i-1].amount,
                    "datetime": str(transaction.added_at),
                    "currency": transaction.currency
                })
        return history
        

class WalletViews(BalanceService):

    async def get_my_balance_view(self, request: Request) -> HTTPResponse:
        return json({
            "status": API_CODES[1000],
            "amount": await self.get_current_balance(
                request.ctx.user,
                request.args.get("currency")
            )
        })
    
    async def add_money_view(self, request: Request) -> HTTPResponse:
        await self.insert_or_spent_money(
            True,
            self.process_currency(request.form.get("currency")),
            float(request.form.get("amount")),
            self.process_tag(request.form.get("tag")),
            request.form.get("description"),
            request.ctx.user
        )
        return json({"status": API_CODES[1000]})
    
    async def spent_money_view(self, request: Request) -> HTTPResponse:
        await self.insert_or_spent_money(
            False,
            self.process_currency(request.form.get("currency")),
            float(request.form.get("amount")),
            self.process_tag(request.form.get("tag")),
            request.form.get("description"),
            request.ctx.user
        )
        return json({"status": API_CODES[1000]})

    async def transaction_history_view(self, request: Request) -> HTTPResponse:
        return json({
            "status": API_CODES[1000],
            "data": await self.get_transaction_history(
                request.args.get("currency"),
                request.ctx.user
            )
        })