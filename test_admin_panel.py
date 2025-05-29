import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdminPanelTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
        
        print("[SETUP] Logging in as admin")
        self.driver.get("http://localhost:3000/login")
        time.sleep(2)
        self.driver.find_element(By.ID, "email_field").send_keys("admin@example.com")
        self.driver.find_element(By.ID, "password_field").send_keys("admin123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
     
        print("[SETUP] Navigating to admin dashboard")
        self.driver.get("http://localhost:3000/admin/dashboard")
        time.sleep(2)

    def test_admin_dashboard(self):
        driver = self.driver
        
        
        print("[DASHBOARD] Verifying dashboard elements")
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".dashboard").is_displayed())
        
        
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".products-section").is_displayed())
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".orders-section").is_displayed())
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".users-section").is_displayed())
        
        print("[DASHBOARD] Dashboard test completed successfully")

    def test_product_management(self):
        driver = self.driver
        
        
        print("[PRODUCTS] Navigating to products list")
        driver.get("http://localhost:3000/admin/products")
        time.sleep(2)
        
      
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".products-table").is_displayed())
        
        
        print("[PRODUCTS] Testing new product creation")
        driver.find_element(By.CSS_SELECTOR, ".new-product-btn").click()
        time.sleep(2)
        
        
        random_num = random.randint(1000, 9999)
        product_name = f"Test Product {random_num}"
        
        print(f"[PRODUCTS] Creating product: {product_name}")
        driver.find_element(By.ID, "name_field").send_keys(product_name)
        driver.find_element(By.ID, "price_field").send_keys("99.99")
        driver.find_element(By.ID, "description_field").send_keys("This is a test product description")
        driver.find_element(By.ID, "category_field").send_keys("Electronics")
        driver.find_element(By.ID, "stock_field").send_keys("50")
        driver.find_element(By.ID, "seller_field").send_keys("Test Seller")
        
        
        print("[PRODUCTS] Submitting product form")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
       
        self.assertIn("success", driver.page_source.lower())
        print("[PRODUCTS] Product management test