import pytest
import requests
import uuid

BASE_URL = "https://qa-scooter.praktikum-services.ru"


@pytest.fixture
def courier():
    # Генерируем уникальные данные курьера
    random_str = str(uuid.uuid4())[:8]
    login = f"student_courier_{random_str}"
    password = f"pass_{random_str}"
    first_name = "Ivan"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Создаем курьера
    response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)
    assert response.status_code == 201

    # Отдаем данные в тест
    yield payload

    # Удаляем курьера после теста
    login_response = requests.post(
        f"{BASE_URL}/api/v1/courier/login",
        json={"login": login, "password": password}
    )
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")