import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

HEADLESS = os.environ.get("HEADLESS", "").lower() in ("true", "1", "yes")
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Selenium photos")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        extra = getattr(report, "extra", [])
        driver = item.funcargs.get("driver")
        if driver:
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"FAIL_{item.name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            driver.save_screenshot(filepath)
            from pytest_html import extras
            extra.append(extras.image(filepath))
            extra.append(extras.text(f"Screenshot guardada: {filename}"))
            report.extra = extra


@pytest.fixture
def driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless")
    if os.path.exists("/usr/bin/firefox"):
        opts.binary_location = "/usr/bin/firefox"
    geckodriver_path = os.environ.get("GECKODRIVER_PATH", "")
    if not geckodriver_path or not os.path.exists(geckodriver_path):
        import shutil
        geckodriver_path = shutil.which("geckodriver") or "/home/crei03/.local/bin/geckodriver"
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service, options=opts)
    driver.maximize_window()
    yield driver
    driver.quit()
