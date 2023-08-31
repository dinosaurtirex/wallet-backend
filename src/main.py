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


app = Sanic("app")


if "Windows" in PLATFORM:
    app.config.OAS = True
else:
    app.config.OAS = False 


app.static(BASE_STATIC_PATH, BASE_STATIC_PATH)
if "Windows" in PLATFORM:
    app.config.CORS_ORIGINS = "http://localhost:3000"
else:
    app.config.CORS_ORIGINS = "*"
app.config.REQUEST_TIMEOUT = 60 * 5
app.config.RESPONSE_TIMEOUT = 60 * 5
app.config.REQUEST_MAX_SIZE = 200_000_000
Extend(app)


@app.on_request
async def run_before_request_handler(request: Request):
    ...


@app.on_response 
async def run_after_request_handler(request: Request, response: HTTPResponse):
    ...


@app.route("/", methods=["GET"])
async def hello_world_view(request: Request) -> HTTPResponse:
    return json({"status": API_CODES[1000]})


#if not "Windows" in PLATFORM: 
@app.exception(Exception)
async def catch_anything(request, exception):
    return json({"status": API_CODES[1001], "error": str( exception )}, status=500)


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