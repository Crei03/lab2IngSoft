from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.driver.maximize_window()

    def enter_username(self, username):
        field = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        field.clear()
        field.send_keys(username)

    def enter_password(self, password):
        field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        field.clear()
        field.send_keys(password)

    def click_login(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        btn.click()

    def get_error_message(self):
        error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error.text

    def get_current_url(self):
        return self.driver.current_url
