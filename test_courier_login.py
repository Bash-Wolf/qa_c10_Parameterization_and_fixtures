import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru"


class TestCourierLogin:

    @pytest.mark.parametrize(
        "login_offset, password_offset, expected_status, expected_body",
        [
            ("valid", "valid", 200, "id"),
            ("empty", "valid", 400, "Недостаточно данных для входа"),
            ("valid", "empty", 400, "Недостаточно данных для входа"),
            ("fake", "fake", 404, "Учетная запись не найдена"),
        ]
    )
    def test_courier_login(self, courier, login_offset, password_offset, expected_status, expected_body):
        # Подставляем логин
        if login_offset == "valid":
            login = courier["login"]
        elif login_offset == "empty":
            login = ""
        else:
            login = "non_existent_login_12345"

        # Подставляем пароль
        if password_offset == "valid":
            password = courier["password"]
        elif password_offset == "empty":
            password = ""
        else:
            password = "wrong_password_12345"

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=payload)

        # Проверяем статус-код
        assert response.status_code == expected_status

        # Проверяем тело ответа
        if expected_status == 200:
            assert expected_body in response.json()
        else:
            assert response.json()["message"] == expected_body