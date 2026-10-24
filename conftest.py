import uuid
import pytest
import requests
from data import Endpoints


@pytest.fixture
def courier():
    """
    Генерирует уникального курьера, регистрирует через API,
    передает credentials в тест, а после выполнения теста удаляет курьера.
    """
    # 1. Генерация уникальных данных
    unique_id = uuid.uuid4().hex[:8]
    login = f"courier_{unique_id}"
    password = f"pass_{unique_id}"
    first_name = f"name_{unique_id}"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # 2. Создание курьера
    response = requests.post(Endpoints.CREATE_COURIER, json=payload)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    # 3. Передача данных в тест
    courier_data = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    yield courier_data

    # 4. Teardown: логинимся, чтобы получить id, и удаляем курьера
    login_response = requests.post(
        Endpoints.LOGIN_COURIER,
        json={"login": login, "password": password}
    )
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{Endpoints.DELETE_COURIER}/{courier_id}")