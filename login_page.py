# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

BASE_URL = "https://www.saucedemo.com/"

class LoginPage(BasePage):
    # ---- locators ----
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_BOX = (By.CSS_SELECTOR, "[data-test='error']")

    # ---- navigation / visibility ----
    def open(self):
        self.go(BASE_URL)
        # page is considered ready when username is visible
        self.wait_visible(self.USERNAME)
        return self

    def is_displayed(self) -> bool:
        return self.is_visible(self.LOGIN_BTN)

    # ---- actions ----
    def fill_username(self, user: str):
        return self.type(self.USERNAME, user)

    def fill_password(self, pwd: str):
        return self.type(self.PASSWORD, pwd)

    def submit(self):
        return self.click(self.LOGIN_BTN)

    def login(self, user: str, pwd: str):
        """Full login flow: open → type creds → submit."""
        return self.open().fill_username(user).fill_password(pwd).submit()

    # ---- assertions helpers ----
    def error_text(self) -> str:
        return self.text_of(self.ERROR_BOX)

    def wait_error_contains(self, snippet: str):
        self.wait.until(EC.text_to_be_present_in_element(self.ERROR_BOX, snippet))
        return self
