# tests/test_cart_pom.py
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

USER = "standard_user"
PASS = "secret_sauce"

ITEMS = [
    ("Sauce Labs Backpack", "sauce-labs-backpack"),
    ("Sauce Labs Bike Light", "sauce-labs-bike-light"),
]

def test_add_two_items_and_remove_all_via_pom(driver):
    # Login
    LoginPage(driver).login(USER, PASS)

    # Inventory page
    inv = InventoryPage(driver).wait_loaded()
    for _, slug in ITEMS:
        inv.add_item(slug)
    inv.wait_badge_equals(2)

    # Open cart
    inv.open_cart()
    cart = CartPage(driver).wait_loaded()

    # Verify both items present
    names_in_cart = set(cart.item_names())
    expected_names = {name for name, _ in ITEMS}
    assert expected_names.issubset(names_in_cart)

    # Remove both
    for _, slug in ITEMS:
        cart.remove_item(slug)

    cart.wait_badge_equals(0)
    assert cart.badge_count() == 0
