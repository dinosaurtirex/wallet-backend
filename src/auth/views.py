from sanic import Request 
from sanic import Blueprint 
from sanic.response import HTTPResponse

from auth.services import AuthServiceViews
from auth.decorators import authorized


auth_bp = Blueprint("auth")


@auth_bp.route("/register", methods=["POST"])
async def register_view(request: Request) -> HTTPResponse:
    return await AuthServiceViews().register_view(request)


@auth_bp.route("/login", methods=["POST"])
async def login_view(request: Request) -> HTTPResponse:
    return await AuthServiceViews().login_view(request)


@auth_bp.route("/logout", methods=["POST"])
@authorized()
async def logout_view(request: Request) -> HTTPResponse:
    return await AuthServiceViews().logout_view(request)


@auth_bp.route("/user_info", methods=["GET"])
@authorized()
async def user_info_view(request: Request) -> HTTPResponse:
    return await AuthServiceViews().user_info_view(request)


@auth_bp.route("/change_password", methods=["PUT"])
@authorized()
async def change_password_view(request: Request) -> HTTPResponse:
    return await AuthServiceViews().change_password_view(request)