import pytest
import requests
from data import Endpoints, ResponseMessages


class TestCourierLogin:

    @pytest.mark.parametrize(
        "case_type, override_login, override_password, expected_status, expected_key, expected_val",
        [
            ("success", None, None, 200, "id", None),
            ("missing_login", "", None, 400, "message", ResponseMessages.INSUFFICIENT_DATA),
            ("missing_password", None, "", 400, "message", ResponseMessages.INSUFFICIENT_DATA),
            ("non_existent", "non_existent_user_99999", "wrong_pass_99999", 404, "message", ResponseMessages.ACCOUNT_NOT_FOUND),
        ],
        ids=[
            "successful_login",
            "login_without_login_field",
            "login_without_password_field",
            "login_with_non_existent_credentials",
        ]
    )
    def test_courier_login_scenarios(
        self,
        courier,
        case_type,
        override_login,
        override_password,
        expected_status,
        expected_key,
        expected_val
    ):
        # Формируем тело запроса на основе созданного фикстурой курьера
        login = courier["login"] if override_login is None else override_login
        password = courier["password"] if override_password is None else override_password

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(Endpoints.LOGIN_COURIER, json=payload)

        # 1. Проверка HTTP статус-кода
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        response_body = response.json()

        # 2. Проверка тела ответа
        if case_type == "success":
            assert expected_key in response_body, f"В теле ответа отсутствует ключ '{expected_key}'"
            assert isinstance(response_body[expected_key], int), f"Поле '{expected_key}' должно быть int"
        else:
            assert response_body.get(expected_key) == expected_val, (
                f"Ожидалось сообщение '{expected_val}', получено '{response_body.get(expected_key)}'"
            )