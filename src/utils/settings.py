import pytz 
import platform 

PLATFORM = platform.platform()

TIMEZONE = pytz.timezone("Europe/Moscow")

DB_URL = f"postgres://wallet_user:69de4794b28b368aec69de4794b2ebef901c1f1968@localhost:5432/wallet_db"

API_CODES = {
    1000: "success",
    1001: "error",
    1002: "not_authorized",
    1003: "invalid_credentials",
    1004: "too_short_password",
    1005: "invalid_currency_provided",
    1006: "provide_currency",
    1007: "not_enough_money"
}

BASE_STATIC_PATH = "static"