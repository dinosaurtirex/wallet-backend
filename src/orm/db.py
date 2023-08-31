import sys 

sys.path.append("../")

from utils.settings import DB_URL


TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "wallet.models"
            ],
            "default_connection": "default",
            "maxsize": 50
        }
    },
    "use_tz": False,
    "timezone": "Europe/Moscow",
}