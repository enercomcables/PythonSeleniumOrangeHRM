
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    INVALID_CREDENTIALS = (
        By.CSS_SELECTOR,
        ".oxd-alert-content-text"
    )

    REQUIRED_ERROR = (
        By.CSS_SELECTOR,
        ".oxd-input-field-error-message"
    )

    def __init__(self, driver, base_url, timeout=10):
        super().__init__(driver, timeout)
        self.base_url = base_url

    def load(self):
        self.open_url(self.base_url)
        self.wait_visible(self.USERNAME)

    def login(self, username, password):
        self.enter_text(self.USERNAME, username)
        self.enter_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.INVALID_CREDENTIALS)

    def get_required_field_errors(self):
        return [
            element.text.strip()
            for element in self.driver.find_elements(
                *self.REQUIRED_ERROR
            )
            if element.is_displayed()
        ]
