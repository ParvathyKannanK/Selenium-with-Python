# tests/test_login_pom.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage

USER = "standard_user"
PASS = "secret_sauce"

def test_login_success_via_pom(driver):
    # use the page object to perform the login
    login = LoginPage(driver)
    login.login(USER, PASS)

    # verify we are on the inventory page
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )
    assert title.text.strip() == "Products"

def test_login_failure_via_pom(driver):
    login = LoginPage(driver).open()
    login.fill_username(USER).fill_password("wrong_password").submit()

    # assert error using page helper
    login.wait_error_contains("Username and password do not match")
