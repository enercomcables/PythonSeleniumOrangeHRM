
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[normalize-space()='Dashboard']"
    )

    USER_DROPDOWN = (
        By.CSS_SELECTOR,
        ".oxd-userdropdown-tab"
    )

    def is_dashboard_displayed(self):
        return self.is_visible(
            self.DASHBOARD_HEADER,
            timeout=10
        )

    def is_user_menu_displayed(self):
        return self.is_visible(
            self.USER_DROPDOWN,
            timeout=5
        )
