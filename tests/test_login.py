
import json
import os
from pathlib import Path

import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utilities.config_reader import get_project_root
from utilities.logger import get_logger


logger = get_logger(__name__)


def load_login_data():
    path = (
        get_project_root()
        / "data"
        / "login_data.json"
    )
    with path.open(encoding="utf-8") as file:
        return json.load(file)


@pytest.mark.smoke
def test_login_with_valid_credentials(driver, config):
    username = os.getenv("ORANGEHRM_USERNAME")
    password = os.getenv("ORANGEHRM_PASSWORD")

    if not username or not password:
        pytest.skip(
            "Set ORANGEHRM_USERNAME and "
            "ORANGEHRM_PASSWORD to run this test"
        )

    login_page = LoginPage(
        driver, config["base_url"], config["timeout"]
    )
    login_page.load()
    login_page.login(username, password)

    dashboard = DashboardPage(
        driver, config["timeout"]
    )

    assert dashboard.is_dashboard_displayed(), (
        "Dashboard was not displayed after login"
    )
    assert dashboard.is_user_menu_displayed(), (
        "User menu was not displayed after login"
    )

    logger.info("Valid login test passed")


@pytest.mark.regression
@pytest.mark.parametrize(
    "test_data",
    load_login_data(),
    ids=lambda data: data["username"]
)
def test_login_with_invalid_credentials(
    driver, config, test_data
):
    login_page = LoginPage(
        driver, config["base_url"], config["timeout"]
    )
    login_page.load()
    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    assert (
        login_page.get_error_message()
        == test_data["expected_error"]
    ), "Expected invalid credentials message was not displayed"


@pytest.mark.regression
def test_login_with_empty_credentials(driver, config):
    login_page = LoginPage(
        driver, config["base_url"], config["timeout"]
    )
    login_page.load()
    login_page.click(login_page.LOGIN_BUTTON)

    errors = login_page.get_required_field_errors()

    assert len(errors) >= 1, (
        "Expected required-field validation messages"
    )
