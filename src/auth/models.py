import pytz 

from tortoise import fields
from tortoise.models import Model

from datetime import datetime 
from datetime import timedelta 


class User(Model):

    id        = fields.IntField(pk=True)
    email     = fields.CharField(max_length=64, unique=True)
    password  = fields.CharField(max_length=128)
    added_at  = fields.DatetimeField(auto_now_add=True)


class Session(Model):

    EXPIRE_HOURS = 24

    id       = fields.IntField(pk=True)
    token    = fields.CharField(max_length=64)
    owner    = fields.ForeignKeyField("models.User")
    added_at = fields.DatetimeField(auto_now_add=True)

    async def is_expired(self) -> bool:
        expire_datetime = self.added_at + timedelta(hours=self.EXPIRE_HOURS)
        return datetime.now(pytz.UTC) > expire_datetime