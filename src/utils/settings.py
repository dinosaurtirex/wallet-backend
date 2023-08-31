import pytz 
import platform 

PLATFORM = platform.platform()

TIMEZONE = pytz.timezone("Europe/Moscow")

DB_URL = f"postgres://admin_user:69de4794b28b368aec69de4794b2ebef901c1f1968@localhost:5432/wallet_db"

API_CODES = {
    1000: "success",
    1001: "error"
}

BASE_STATIC_PATH = "static"