import re
import uuid 
import random 
import string
from sanic import Request 
from sanic import Blueprint 
from sanic.response import json 
from sanic.response import HTTPResponse

from auth.models import Session
from auth.models import User
from utils.settings import API_CODES


def generate_uuid(length: int=16) -> str:
    if length > 128:
        raise ValueError("uuid > 128")
    huge_uuid = ""
    for _ in range(10):
        huge_uuid += str(uuid.uuid4()).replace("-","")
    return huge_uuid[:length]


async def check_auth_and_get_user_from_request(token: str) -> tuple[bool, User | None]:
    user_session = await Session.get_or_none(token=token)
    if user_session is None:
        return (False, None)
    if not await user_session.is_expired():
        return (True, await user_session.owner)
    return (False, None)


class AuthService:

    def __is_valid_email(self, email: str) -> bool:
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)
    
    def generate_password(self, length: int=8) -> str:
        return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

    async def register(self, email: str) -> User:
        user_instance = await User.get_or_none(email=email)
        if user_instance is not None:
            raise ValueError(API_CODES[1003])
        if not self.__is_valid_email(email):
            raise ValueError(API_CODES[1003])
        return await User.create(email=email, password=self.generate_password())

    async def login(self, email: str, password: str) -> Session:
        user_instance = await User.get_or_none(email=email, password=password)
        if user_instance is None:
            raise ValueError(API_CODES[1003])
        new_session = await Session.create(
            token = generate_uuid(32),
            owner = user_instance
        )
        return new_session.token
    
    async def logout(self, email: str | None, password: str | None, owner: User | None) -> None:
        user_instance = owner 
        if user_instance is None:
            user_instance = await User.get_or_none(email=email, password=password)
            if user_instance is None:
                raise ValueError(API_CODES[1003])
        for session in await Session.filter(owner=user_instance):
            await session.delete()


class AuthServiceViews(AuthService):

    async def register_view(self, request: Request) -> HTTPResponse:
        new_user = await self.register(request.form.get("email"))
        return json({
            "status": API_CODES[1000],
            "id": new_user.id,
            "generated_password": new_user.password,
            "token": await self.login(request.form.get("email"), new_user.password)
        })
    
    async def login_view(self, request: Request) -> HTTPResponse:
        return json({
            "status": API_CODES[1000],
            "token": await self.login(request.form.get("email"), request.form.get("password"))
        })
    
    async def logout_view(self, request: Request) -> HTTPResponse:
        await self.logout(None, None, request.ctx.user)
        return json({
            "status": API_CODES[1000]
        })
    
    async def user_info_view(self, request: Request) -> HTTPResponse:
        return json({
            "status": API_CODES[1000],
            "email": request.ctx.user.email
        })
    
    async def change_password_view(self, request: Request) -> HTTPResponse:
        if len(request.form.get("new_password")) < 6:
            raise ValueError(API_CODES[1004])
        request.ctx.user.password = request.form.get("new_password")
        await request.ctx.user.save()
        return json({"status": API_CODES[1000]})