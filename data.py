import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://qa-scooter.praktikum-services.ru")

class Endpoints:
    CREATE_COURIER = f"{BASE_URL}/api/v1/courier"
    LOGIN_COURIER = f"{BASE_URL}/api/v1/courier/login"
    DELETE_COURIER = f"{BASE_URL}/api/v1/courier"

class ResponseMessages:
    INSUFFICIENT_DATA = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"