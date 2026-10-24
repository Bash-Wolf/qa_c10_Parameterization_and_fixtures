import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


@pytest.fixture
def courier():
    # 1. Генерируем уникальный логин курьера с помощью uuid
    login = f"courier_{uuid.uuid4().hex[:8]}"

    courier_data = {
        "login": login,
        "password": "Password123!",
        "firstName": "TestCourier",
    }

    # 2. Создаем курьера через POST /api/v1/courier
    response = requests.post(
        f"{BASE_URL}/api/v1/courier",
        json=courier_data,
    )
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    # 3. Авторизуемся для получения courier_id
    login_response = requests.post(
        f"{BASE_URL}/api/v1/courier/login",
        json={
            "login": courier_data["login"],
            "password": courier_data["password"],
        },
    )
    assert login_response.status_code == 200, f"Не удалось авторизоваться для получения id: {login_response.text}"
    courier_id = login_response.json().get("id")

    # 4. Передаем в тест данные курьера и полученный id
    yield {
        "login": courier_data["login"],
        "password": courier_data["password"],
        "id": courier_id,
    }

    # 5. Teardown: после завершения теста удаляем созданного курьера
    if courier_id:
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")