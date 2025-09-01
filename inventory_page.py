# pages/inventory_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.common.exceptions import TimeoutException


class InventoryPage(BasePage):
    # ---- page + header/cart locators ----
    TITLE = (By.CLASS_NAME, "title")                     # should read "Products"
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    # ---- menu / logout locators ----
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    MENU_WRAP = (By.CSS_SELECTOR, ".bm-menu-wrap")       # sliding drawer container
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # ---- per-item helpers (use stable data-test slugs) ----
    def _add_btn(self, slug: str):
        return (By.CSS_SELECTOR, f"button[data-test='add-to-cart-{slug}']")

    def _remove_btn(self, slug: str):
        return (By.CSS_SELECTOR, f"button[data-test='remove-{slug}']")

    # ---- page checks ----
    def wait_loaded(self):
        self.wait.until(EC.url_contains("inventory.html"))
        self.wait_visible(self.TITLE)
        return self

    def title_text(self) -> str:
        return self.text_of(self.TITLE)

    # ---- actions: add/remove items ----
    def add_item(self, slug: str):
        """
        Add an item by slug, e.g. 'sauce-labs-backpack'.
        Scrolls into view, clicks (with JS fallback), waits for 'Remove' state, and best-effort badge +1.
        """
        add_sel = self._add_btn(slug)
        remove_sel = self._remove_btn(slug)

        before = self.badge_count()

        add_btn = self.wait_clickable(add_sel)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
        try:
            add_btn.click()
        except Exception:
            # animation/overlay can intercept; JS click is reliable
            self.driver.execute_script("arguments[0].click();", add_btn)

        # presence (not visibility) right after state flip is more robust
        self.wait.until(EC.presence_of_element_located(remove_sel))

        # optional: confirm badge increment (don’t fail test if it lags)
        try:
            self.wait.until(lambda d: self.badge_count() == before + 1)
        except Exception:
            pass

        return self

    def remove_item(self, slug: str):
        """
        Remove an item by slug. Confirms state flips back to 'Add'.
        """
        remove_sel = self._remove_btn(slug)
        add_sel = self._add_btn(slug)

        btn = self.wait_clickable(remove_sel)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        self.wait.until(EC.presence_of_element_located(add_sel))
        return self

    # ---- cart actions / badge helpers ----
    def open_cart(self):
        self.click(self.CART_LINK)
        self.wait.until(EC.url_contains("cart.html"))
        return self

    def badge_count(self) -> int:
        """
        Current cart badge number (0 if hidden).
        """
        els = self.driver.find_elements(*self.CART_BADGE)
        if not els:
            return 0
        txt = els[0].text.strip()
        return int(txt) if txt.isdigit() else 0

    def wait_badge_equals(self, n: int):
        self.wait.until(lambda d: self.badge_count() == n)
        return self

    # ---- menu + logout flow ----
    def open_menu(self):
        """
        Open the left burger menu and wait until the Logout link is actually visible.
        Retries with JS click if the first click is swallowed by animation.
        """
        btn = self.wait_clickable(self.MENU_BTN)
        try:
           btn.click()
           # Wait directly for the actionable thing: the Logout link
           self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        except TimeoutException:
           # Retry with JS click in case the first click was intercepted
           self.driver.execute_script("arguments[0].click();", btn)
           self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        return self

    def logout(self):
       """
       Click Logout safely and verify we’re back on the login page.
       """
       link = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
       # JS click avoids rare animation/overlay intercepts
       self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
       self.driver.execute_script("arguments[0].click();", link)

       # Strong proof we’re on the login page
       from selenium.webdriver.common.by import By as _By
       self.wait.until(EC.visibility_of_element_located((_By.ID, "login-button")))
       return self
