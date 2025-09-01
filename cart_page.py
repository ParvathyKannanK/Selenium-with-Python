# pages/cart_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class CartPage(BasePage):
    # ---- locators ----
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def wait_loaded(self):
        self.wait.until(EC.url_contains("cart.html"))
        self.wait_visible(self.ITEM_NAMES)  # at least one item visible
        return self

    def item_names(self) -> list[str]:
        """Return all item names currently in the cart."""
        return [el.text.strip() for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove_item(self, slug: str):
        """Remove an item using its slug (same as InventoryPage)."""
        remove_sel = (By.CSS_SELECTOR, f"button[data-test='remove-{slug}']")
        btn = self.wait_clickable(remove_sel)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)
        return self

    def badge_count(self) -> int:
        els = self.driver.find_elements(*self.CART_BADGE)
        if not els:
            return 0
        txt = els[0].text.strip()
        return int(txt) if txt.isdigit() else 0

    def wait_badge_equals(self, n: int):
        self.wait.until(lambda d: self.badge_count() == n)
        return self
