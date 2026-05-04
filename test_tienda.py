import os
import pytest
from datetime import datetime
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Selenium photos")


def snap(driver, name):
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{timestamp}_{name}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"  [Captura] {filename}")
    return filename


class TestTiendaSaucedemo:

    def test_login_exitoso(self, driver):
        """Caso 1: Login exitoso con credenciales válidas"""
        print("\n=== CASO 1: Login exitoso ===")
        login = LoginPage(driver)

        login.open()
        snap(driver, "01_login_page")

        login.enter_username("standard_user")
        snap(driver, "02_username_entered")

        login.enter_password("secret_sauce")
        snap(driver, "03_password_entered")

        login.click_login()
        snap(driver, "04_after_login_click")

        inventory = InventoryPage(driver)
        inventory.wait_for_load()
        snap(driver, "05_inventory_page")

        assert inventory.is_on_inventory_page(), \
            f"No redirigió a inventory. URL actual: {login.get_current_url()}"
        print("  RESULTADO: PASS - Login exitoso verificado")

    def test_agregar_carrito(self, driver):
        """Caso 2: Agregar producto al carrito y validar badge"""
        print("\n=== CASO 2: Agregar producto al carrito ===")
        login = LoginPage(driver)
        login.open()
        login.enter_username("standard_user")
        login.enter_password("secret_sauce")
        login.click_login()

        inventory = InventoryPage(driver)
        inventory.wait_for_load()
        snap(driver, "06_inventory_loaded")

        inventory.add_backpack_to_cart()
        snap(driver, "07_after_add_to_cart")

        cart_count = inventory.get_cart_count()
        snap(driver, "08_cart_badge")

        assert cart_count == 1, \
            f"Se esperaba 1 producto en el carrito, se obtuvo: {cart_count}"
        print(f"  RESULTADO: PASS - Carrito muestra {cart_count} producto(s)")

    def test_login_fallido_bloqueado(self, driver):
        """Caso 3: Login fallido con usuario bloqueado (locked_out_user)"""
        print("\n=== CASO 3: Login fallido (usuario bloqueado) ===")
        login = LoginPage(driver)

        driver.delete_all_cookies()
        login.open()
        snap(driver, "09_login_page_bloqueado")

        login.enter_username("locked_out_user")
        snap(driver, "10_username_locked_entered")

        login.enter_password("secret_sauce")
        snap(driver, "11_password_locked_entered")

        login.click_login()
        snap(driver, "12_after_locked_login")

        error_text = login.get_error_message()
        snap(driver, "13_error_message_locked")

        assert "Sorry, this user has been locked out" in error_text, \
            f"Mensaje de error inesperado: {error_text}"
        print(f"  RESULTADO: PASS - Mensaje validado: {error_text}")
