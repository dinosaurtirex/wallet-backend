from sanic import Sanic
from sanic import Request 
from sanic.response import HTTPResponse
from sanic.response import json 
from sanic_ext import Extend
from tortoise.contrib.sanic import register_tortoise

from utils.settings import BASE_STATIC_PATH
from utils.settings import API_CODES
from utils.settings import PLATFORM
from orm.db import TORTOISE_ORM
from auth.services import check_auth_and_get_user_from_request

from wallet.views import wallet_bp
from auth.views import auth_bp


app = Sanic("wallet_backend")

app.blueprint(auth_bp)
app.blueprint(wallet_bp)


app.static(BASE_STATIC_PATH, BASE_STATIC_PATH)

app.config.OAS = False 
app.config.CORS_ORIGINS = "*"
app.config.REQUEST_TIMEOUT = 60 * 5
app.config.RESPONSE_TIMEOUT = 60 * 5
app.config.REQUEST_MAX_SIZE = 200_000_000

Extend(app)


@app.on_request
async def run_before_request_handler(request: Request):
    is_authenticated, user_instance = \
        await check_auth_and_get_user_from_request(
            request.token
        )
    request.ctx.is_authenticated = is_authenticated
    if is_authenticated:
        request.ctx.user = user_instance


@app.on_response 
async def run_after_request_handler(request: Request, response: HTTPResponse):
    ...


@app.route("/", methods=["GET"])
async def hello_world_view(request: Request) -> HTTPResponse:
    return json({"status": API_CODES[1000]})



# @app.exception(Exception)
async def catch_anything(request, exception):
     return json({
         "status": API_CODES[1001], 
         "error": str( exception )
     }, status=500)


register_tortoise(
    app,
    config=TORTOISE_ORM
)


if __name__ == "__main__":
    dev = False
    if "Windows" in PLATFORM:
        dev = True
    app.run(
        host="localhost", 
        port=1000, 
        dev=dev,
        access_log=False
    )
