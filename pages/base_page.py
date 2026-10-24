
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.logger import get_logger


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.logger = get_logger(self.__class__.__name__)

    def open_url(self, url):
        self.driver.get(url)
        self.logger.info("Opened URL: %s", url)

    def wait_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    def enter_text(self, locator, value):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(value)
        self.logger.info("Entered text into %s", locator)

    def click(self, locator):
        self.wait_clickable(locator).click()
        self.logger.info("Clicked element: %s", locator)

    def get_text(self, locator):
        return self.wait_visible(locator).text.strip()

    def is_visible(self, locator, timeout=None):
        try:
            wait = WebDriverWait(
                self.driver,
                timeout or 3
            )
            wait.until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False
