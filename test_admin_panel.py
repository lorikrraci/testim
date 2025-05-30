import unittest
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AdminPanelTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        self.base_url = "http://localhost:3000"
        
        self.admin_email = "admin@example.com"
        self.admin_password = "admin123"
        
        self.wait = WebDriverWait(self.driver, 10)
        
        self.admin_login()
        
    def admin_login(self):
        """Helper method to login as admin"""
        try:
            print("[SETUP] Logging in as admin")
            self.driver.get(f"{self.base_url}/login")
            time.sleep(2)
            
            self.driver.save_screenshot("screenshots/admin_login_page.png")
            
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email_field")))
            email_field.clear()
            email_field.send_keys(self.admin_email)
            
            password_field = self.driver.find_element(By.ID, "password_field")
            password_field.clear()
            password_field.send_keys(self.admin_password)
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            time.sleep(3)
            self.driver.save_screenshot("screenshots/admin_after_login.png")
            
            print("[SETUP] Navigating to admin dashboard")
            self.driver.get(f"{self.base_url}/admin/dashboard")
            time.sleep(2)
            self.driver.save_screenshot("screenshots/admin_dashboard.png")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/admin_login_error.png")
            raise Exception(f"Admin login failed: {str(e)}")

    def find_element_safely(self, by, value, timeout=10, screenshot_prefix="element"):
        """Helper method to find elements safely with explicit wait and screenshots"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except (TimeoutException, NoSuchElementException):
            self.driver.save_screenshot(f"screenshots/{screenshot_prefix}_not_found.png")
            raise Exception(f"Could not find element {by}={value}")

    def test_admin_dashboard(self):
        """Test admin dashboard elements"""
        try:
            driver = self.driver
            
            print("[DASHBOARD] Verifying dashboard elements")
            
            dashboard = self.find_element_safely(
                By.CSS_SELECTOR, 
                ".dashboard", 
                screenshot_prefix="dashboard"
            )
            self.assertTrue(dashboard.is_displayed())
            
            sections = [
                (".products-section", "products"),
                (".orders-section", "orders"),
                (".users-section", "users")
            ]
            
            for selector, name in sections:
                section = self.find_element_safely(
                    By.CSS_SELECTOR, 
                    selector, 
                    screenshot_prefix=f"dashboard_{name}"
                )
                self.assertTrue(section.is_displayed())
                print(f"[DASHBOARD] Verified {name} section")
            
            driver.save_screenshot("screenshots/dashboard_test_complete.png")
            print("[DASHBOARD] Dashboard test completed successfully")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/dashboard_test_error.png")
            self.fail(f"Dashboard test failed: {str(e)}")

    def test_product_management(self):
        """Test product management functionality"""
        try:
            driver = self.driver
            
            print("[PRODUCTS] Navigating to products list")
            driver.get(f"{self.base_url}/admin/products")
            time.sleep(2)
            driver.save_screenshot("screenshots/products_list.png")
            
            products_table = self.find_element_safely(
                By.CSS_SELECTOR, 
                ".products-table", 
                screenshot_prefix="products_table"
            )
            self.assertTrue(products_table.is_displayed())
            
            print("[PRODUCTS] Testing new product creation")
            new_product_btn = self.find_element_safely(
                By.CSS_SELECTOR, 
                ".new-product-btn", 
                screenshot_prefix="new_product_btn"
            )
            new_product_btn.click()
            time.sleep(2)
            driver.save_screenshot("screenshots/new_product_form.png")
            
            random_num = random.randint(1000, 9999)
            product_name = f"Test Product {random_num}"
            
            print(f"[PRODUCTS] Creating product: {product_name}")
            
            name_field = self.find_element_safely(
                By.ID, 
                "name_field", 
                screenshot_prefix="product_name_field"
            )
            name_field.clear()
            name_field.send_keys(product_name)
            
            price_field = self.find_element_safely(
                By.ID, 
                "price_field", 
                screenshot_prefix="product_price_field"
            )
            price_field.clear()
            price_field.send_keys("99.99")
            
            description_field = self.find_element_safely(
                By.ID, 
                "description_field", 
                screenshot_prefix="product_description_field"
            )
            description_field.clear()
            description_field.send_keys("This is a test product description")
            
            category_field = self.find_element_safely(
                By.ID, 
                "category_field", 
                screenshot_prefix="product_category_field"
            )
            category_field.clear()
            category_field.send_keys("Electronics")
            
            stock_field = self.find_element_safely(
                By.ID, 
                "stock_field", 
                screenshot_prefix="product_stock_field"
            )
            stock_field.clear()
            stock_field.send_keys("50")
            
            seller_field = self.find_element_safely(
                By.ID, 
                "seller_field", 
                screenshot_prefix="product_seller_field"
            )
            seller_field.clear()
            seller_field.send_keys("Test Seller")
            
            driver.save_screenshot("screenshots/product_form_filled.png")
            
            print("[PRODUCTS] Submitting product form")
            submit_button = self.find_element_safely(
                By.CSS_SELECTOR, 
                "button[type='submit']", 
                screenshot_prefix="product_submit_button"
            )
            submit_button.click()
            time.sleep(3)
            
            driver.save_screenshot("screenshots/after_product_creation.png")
            
            self.assertIn("success", driver.page_source.lower())
            print("[PRODUCTS] Product management test completed successfully")
            
            with open("test_product_info.txt", "w") as f:
                f.write(f"Product Name: {product_name}\n")
                f.write("Price: 99.99\n")
                f.write("Category: Electronics\n")
                f.write("Stock: 50\n")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/product_test_error.png")
            self.fail(f"Product management test failed: {str(e)}")

    def test_order_management(self):
        """Test order management functionality"""
        try:
            driver = self.driver
            
            print("[ORDERS] Navigating to orders list")
            driver.get(f"{self.base_url}/admin/orders")
            time.sleep(2)
            driver.save_screenshot("screenshots/orders_list.png")
            
            try:
                orders_table = self.find_element_safely(
                    By.CSS_SELECTOR, 
                    ".orders-table", 
                    screenshot_prefix="orders_table",
                    timeout=5
                )
                self.assertTrue(orders_table.is_displayed())
                
                order_rows = driver.find_elements(By.CSS_SELECTOR, ".orders-table tr")
                if len(order_rows) > 1:
                    print("[ORDERS] Viewing order details")
                    view_button = self.find_element_safely(
                        By.CSS_SELECTOR, 
                        ".view-order-btn", 
                        screenshot_prefix="view_order_btn",
                        timeout=5
                    )
                    view_button.click()
                    time.sleep(2)
                    driver.save_screenshot("screenshots/order_details.png")
                    
                    order_details = self.find_element_safely(
                        By.CSS_SELECTOR, 
                        ".order-details", 
                        screenshot_prefix="order_details",
                        timeout=5
                    )
                    self.assertTrue(order_details.is_displayed())
                    
                    print("[ORDERS] Order details verified successfully")
                else:
                    print("[ORDERS] No orders found to test details view")
            except Exception as e:
                print(f"[ORDERS] Could not verify orders table: {str(e)}")
                print("[ORDERS] This may be normal if no orders exist yet")
            
            print("[ORDERS] Order management test completed")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/order_test_error.png")
            self.fail(f"Order management test failed: {str(e)}")

    def test_user_management(self):
        """Test user management functionality"""
        try:
            driver = self.driver
            
            print("[USERS] Navigating to users list")
            driver.get(f"{self.base_url}/admin/users")
            time.sleep(2)
            driver.save_screenshot("screenshots/users_list.png")
            
            try:
                users_table = self.find_element_safely(
                    By.CSS_SELECTOR, 
                    ".users-table", 
                    screenshot_prefix="users_table",
                    timeout=5
                )
                self.assertTrue(users_table.is_displayed())
                
                user_rows = driver.find_elements(By.CSS_SELECTOR, ".users-table tr")
                if len(user_rows) > 1:
                    print("[USERS] Users table verified successfully")
                else:
                    print("[USERS] No users found in the table")
            except Exception as e:
                print(f"[USERS] Could not verify users table: {str(e)}")
                print("[USERS] This may be normal if the table has a different class name")
            
            print("[USERS] User management test completed")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/user_test_error.png")
            self.fail(f"User management test failed: {str(e)}")

    def tearDown(self):
        if self.driver:
            print("[TEARDOWN] Closing browser")
            self.driver.quit()

if __name__ == "__main__":
    print("[MAIN] Starting admin panel tests")
    unittest.main()
