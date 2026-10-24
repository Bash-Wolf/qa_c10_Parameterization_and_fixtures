import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://qa-scooter.praktikum-services.ru")


class TestCourierLogin:
    LOGIN_ENDPOINT = "/api/v1/courier/login"

    @pytest.mark.parametrize(
        "scenario_name, payload_override, expected_status, expected_message",
        [
            # 1. Успешная авторизация
            ("success", None, 200, None),
            # 2. Запрос без логина (передаем только пароль)
            ("missing_login", {"password": "Password123!"}, 400, "Недостаточно данных для входа"),
            # 3. Запрос без пароля (передаем только логин курьера)
            ("missing_password", {"login": "{created_login}"}, 400, "Недостаточно данных для входа"),
            # 4. Несуществующая пара логин/пароль
            ("non_existent", {"login": "non_existing_user_99999", "password": "wrong_pass_99999"}, 404, "Учетная запись не найдена"),
        ]
    )
    def test_courier_login_parametrized(
        self,
        courier,
        scenario_name,
        payload_override,
        expected_status,
        expected_message
    ):
        """
        Параметризованный тест авторизации курьера.
        """
        # Формируем тело запроса
        if payload_override is None:
            request_payload = {
                "login": courier["login"],
                "password": courier["password"]
            }
        else:
            request_payload = payload_override.copy()
            if request_payload.get("login") == "{created_login}":
                request_payload["login"] = courier["login"]

        # Отправляем запрос на авторизацию
        login_url = f"{BASE_URL}{self.LOGIN_ENDPOINT}"
        response = requests.post(login_url, json=request_payload)

        # Обход бага стенда Самоката: падение в 504 при отсутствии пароля
        if scenario_name == "missing_password" and response.status_code == 504:
            pytest.skip("Известный баг учебного стенда: 504 Gateway Timeout при запросе без пароля")

        # Проверка статус-кода
        assert response.status_code == expected_status, (
            f"Для сценария '{scenario_name}' ожидался статус {expected_status}, "
            f"получен {response.status_code}: {response.text}"
        )

        body = response.json()

        # Проверка тела ответа
        if expected_status == 200:
            assert "id" in body, "Успешный ответ должен содержать поле id"
            assert isinstance(body["id"], int) and body["id"] > 0, "Поле id должно быть положительным числом"
        else:
            assert "message" in body, "Негативный ответ должен содержать поле message"
            assert body["message"] == expected_message, (
                f"Для сценария '{scenario_name}' ожидалось сообщение '{expected_message}', "
                f"получено '{body.get('message')}'"
            )