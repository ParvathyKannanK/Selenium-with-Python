# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

class BasePage:
    def __init__(self, driver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---- generic helpers ----
    def go(self, url: str):
        self.driver.get(url)
        return self

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        el = self.wait_clickable(locator)
        el.click()
        return self

    def js_click(self, locator):
        el = self.wait_visible(locator)
        self.driver.execute_script("arguments[0].click();", el)
        return self

    def type(self, locator, text: str, clear_first: bool = True):
        el = self.wait_visible(locator)
        if clear_first:
            el.clear()
        el.send_keys(text)
        return self

    def text_of(self, locator) -> str:
        return self.wait_visible(locator).text.strip()

    def is_visible(self, locator) -> bool:
        try:
            self.wait_visible(locator)
            return True
        except Exception:
            return False
