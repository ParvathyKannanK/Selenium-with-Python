# tests/test_inventory_pom.py
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

USER = "standard_user"
PASS = "secret_sauce"

def test_add_and_remove_backpack_via_pom(driver):
    login = LoginPage(driver)
    login.login(USER, PASS)

    inv = InventoryPage(driver).wait_loaded()
    assert inv.title_text() == "Products"

    # Add one item
    inv.add_item("sauce-labs-backpack").wait_badge_equals(1)

    # Remove it
    inv.remove_item("sauce-labs-backpack")
    inv.wait_badge_equals(0)
