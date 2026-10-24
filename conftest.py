
import pytest
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from utilities.config_reader import load_config, get_project_root
from utilities.logger import get_logger


logger = get_logger(__name__)


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture
def driver(request, config):
    browser = config["browser"]

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if config["headless"]:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        web_driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if config["headless"]:
            options.add_argument("-headless")
        web_driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(
            f"Unsupported browser: {browser}"
        )

    web_driver.implicitly_wait(0)
    web_driver.set_page_load_timeout(
        config["page_load_timeout"]
    )

    request.node._webdriver = web_driver

    yield web_driver

    web_driver.quit()
    logger.info("Browser session closed")


@pytest.fixture
def wait(driver, config):
    return WebDriverWait(driver, config["timeout"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver = getattr(item, "_webdriver", None)
    if driver is None:
        return

    screenshot_dir = (
        get_project_root() / "screenshots"
    )
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(
        c if c.isalnum() or c in "-_" else "_"
        for c in item.nodeid
    )
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    path = screenshot_dir / (
        f"{safe_name}_{timestamp}.png"
    )

    try:
        driver.save_screenshot(str(path))
        logger.error("Failure screenshot saved: %s", path)
        item._screenshot_path = str(path)
    except Exception:
        logger.exception("Could not save failure screenshot")
