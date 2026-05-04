from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_load(self):
        self.wait.until(EC.presence_of_element_located(self.INVENTORY_CONTAINER))

    def is_on_inventory_page(self):
        return "inventory.html" in self.driver.current_url

    def add_backpack_to_cart(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BACKPACK))
        btn.click()

    def get_cart_count(self):
        elements = self.driver.find_elements(*self.CART_BADGE)
        if elements:
            return int(elements[0].text)
        return 0
