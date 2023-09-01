from sanic import Request 
from sanic import Blueprint 
from sanic.response import HTTPResponse

from auth.decorators import authorized

from wallet.services import WalletViews


wallet_bp = Blueprint("wallet")


@wallet_bp.route("/get/balance", methods=["GET"])
@authorized()
async def get_my_balance_view(request: Request) -> HTTPResponse:
    return await WalletViews().get_my_balance_view(request)


@wallet_bp.route("/add/balance", methods=["POST"])
@authorized()
async def add_money_view(request: Request) -> HTTPResponse:
    return await WalletViews().add_money_view(request)


@wallet_bp.route("/spent/balance", methods=["POST"])
@authorized()
async def spent_money_view(request: Request) -> HTTPResponse:
    return await WalletViews().spent_money_view(request)
