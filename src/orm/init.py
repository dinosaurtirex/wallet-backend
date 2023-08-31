from tortoise import Tortoise

from orm.db import TORTOISE_ORM
from orm.db import DB_URL


async def init():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": TORTOISE_ORM["apps"]["models"]["models"]}
    )
    await Tortoise.generate_schemas()