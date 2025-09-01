# tests/test_logout_pom.py
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

USER = "standard_user"
PASS = "secret_sauce"

def test_logout_via_pom(driver):
    # login
    LoginPage(driver).login(USER, PASS)

    # open menu and logout
    inv = InventoryPage(driver).wait_loaded()
    inv.open_menu().logout()

    # final assertion: back on login page
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    login_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "login-button")))
    assert login_btn.is_displayed()
