Selenium + Python Automated Tests (POM) — SauceDemo  

A clean, reproducible Selenium WebDriver + Python + pytest** suite that tests the e-commerce demo site [saucedemo.com] (https://www.saucedemo.com).  

---

Features Covered
- Login (success & failure)  
- Add to Cart (single & multiple items)  
- Cart validation (names, badge)  
- Logout  
- Page Object Model (POM) for maintainability  

---

Highlights
- Stable locators using `data-test` attributes  
- Explicit waits + JS click fallbacks to avoid animation flakiness  
- Pytest fixtures (`conftest.py`) for a shared, headless-ready Chrome setup  
- CI-friendly structure  

---

Tech & Versions
- Python 3.x  
- Selenium 4.x  
- webdriver-manager 4.x  
- pytest 8.x  

---

Project Structure

AutomatedTests-Selenium/
├─ pages/
│  ├─ __init__.py
│  ├─ base_page.py
│  ├─ login_page.py
│  ├─ inventory_page.py
│  └─ cart_page.py
├─ tests/
│  ├─ test_login_pom.py
│  ├─ test_inventory_pom.py
│  ├─ test_cart_pom.py
│  └─ test_logout_pom.py
├─ conftest.py
├─ requirements.txt
├─ pytest.ini
└─ README.md

---

Setup

1)	Create & activate virtual environment
python -m venv .venv
Windows
.\.venv\Scripts\activate
macOS/Linux
source .venv/bin/activate

2)	Install dependencies
pip install -r requirements.txt
or
pip install selenium webdriver-manager pytest pytest-html

---

Running Tests

Run all tests : pytest -q
Run one test file: pytest tests/test_cart_pom.py -q
Run one test function: pytest tests/test_cart_pom.py::test_add_two_items_and_remove_all_via_pom -q
Generate HTML report: pytest --html=report.html --self-contained-html

---

What the Tests Do

1) Login (success & failure)
   
Success: logs in with standard_user / secret_sauce, asserts Products title.
Failure: wrong password, asserts error text appears ([data-test='error']).

Key locators:
Username: #user-name
Password: #password
Login button: #login-button
Error box: [data-test='error']
File: tests/test_login_pom.py

2) Inventory (add/remove single item)

Adds Sauce Labs Backpack, asserts cart badge = 1
Removes it, asserts badge disappears

Key locators:
Add: button[data-test='add-to-cart-sauce-labs-backpack']
Remove: button[data-test='remove-sauce-labs-backpack']
Badge: .shopping_cart_badge
File: tests/test_inventory_pom.py

3) Cart (two items + validation)

Adds Backpack + Bike Light
Asserts badge = 2
Opens cart, asserts both item names present
Removes both, asserts badge disappears

Key locators:
Cart link: a.shopping_cart_link
Item names: .inventory_item_name
Badge: .shopping_cart_badge
File: tests/test_cart_pom.py

4) Logout
   
Opens burger menu, clicks Logout
Asserts login button is visible again

Key locators:
Menu button: #react-burger-menu-btn
Logout link: #logout_sidebar_link
File: tests/test_logout_pom.py

---

Page Object Model (POM)

Keep selectors & low-level actions inside pages, so tests read like intent.
•	BasePage: shared waits & helpers (wait_visible, click, type, badge_count, etc.)
•	LoginPage: open(), login(user, pass), error helpers
•	InventoryPage: add_item(slug), remove_item(slug), wait_badge_equals(n), open_cart(), open_menu(), logout()
•	CartPage: item_names(), remove_item(slug), wait_badge_equals(n)

Example (from tests/test_cart_pom.py):

LoginPage(driver).login("standard_user", "secret_sauce")
inv = InventoryPage(driver).wait_loaded()
inv.add_item("sauce-labs-backpack").add_item("sauce-labs-bike-light").wait_badge_equals(2)
inv.open_cart()
cart = CartPage(driver).wait_loaded()
assert {"Sauce Labs Backpack", "Sauce Labs Bike Light"}.issubset(set(cart.item_names()))
for slug in ["sauce-labs-backpack", "sauce-labs-bike-light"]:
    cart.remove_item(slug)
cart.wait_badge_equals(0)

Fixture: driver (Chrome, headless-ready)
conftest.py

import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # enable for CI
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())
    drv = Chrome(service=service, options=options)
    yield drv
    drv.quit()

---

Results (sample)
....
4 passed in 20.7s

---

Next Ideas
•	Add Checkout flow (“THANK YOU FOR YOUR ORDER!”)
•	Parameterize items/users
•	Parallel runs (pytest -n auto with pytest-xdist)
•	Allure or richer HTML reporting
•	GitHub Actions workflow to run on every push (upload report.html)

This project was created to practice and demonstrate professional-grade test automation skills with Selenium, Python, and PyTest, using industry patterns such as POM and CI-ready workflows.




