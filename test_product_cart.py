import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductCartTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://localhost:3000")
        time.sleep(1)

    def test_product_search(self):
        driver = self.driver
      
        print("[SEARCH] Testing product search")
        search_box = driver.find_element(By.ID, "search_field")
        search_box.clear()
        search_box.send_keys("laptop")
        driver.find_element(By.ID, "search_btn").click()
        time.sleep(2)
        
        
        self.assertIn("laptop", driver.page_source.lower())
        print("[SEARCH] Search test completed successfully")

    def test_product_details(self):
        driver = self.driver
        
      
        print("[DETAILS] Navigating to product details")
        driver.get("http://localhost:3000/product/123")
        time.sleep(2)
        
        
        product_name = driver.find_element(By.CSS_SELECTOR, "h3").text
        self.assertTrue(len(product_name) > 0)
        self.assertTrue(driver.find_element(By.ID, "product_price").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "cart_btn").is_displayed())
        print(f"[DETAILS] Product details test completed for: {product_name}")

    def test_add_to_cart(self):
        driver = self.driver
        
        
        print("[CART] Navigating to product")
        driver.get("http://localhost:3000/product/123")
        time.sleep(2)
        
        
        product_name = driver.find_element(By.CSS_SELECTOR, "h3").text
        
     
        print("[CART] Increasing quantity")
        driver.find_element(By.CSS_SELECTOR, "span.btn.btn-primary.plus").click()
        time.sleep(1)
        
        
        print("[CART] Adding to cart")
        driver.find_element(By.ID, "cart_btn").click()
        time.sleep(2)
        
      
        self.assertIn("Item Added to Cart", driver.page_source)
        print("[CART] Add to cart test completed successfully")

    def test_cart_operations(self):
        driver = self.driver
        
    
        print("[CART-OPS] Adding product to cart first")
        driver.get("http://localhost:3000/product/123")
        time.sleep(2)
        driver.find_element(By.ID, "cart_btn").click()
        time.sleep(2)
        
       
        print("[CART-OPS] Navigating to cart page")
        driver.get("http://localhost:3000/cart")
        time.sleep(2)
        
       
        self.assertNotIn("Your Cart is Empty", driver.page_source)
        
        
        if "Your Cart is Empty" not in driver.page_source:
            print("[CART-OPS] Testing remove from cart")
            remove_buttons = driver.find_elements(By.CSS_SELECTOR, ".fa-trash")
            if len(remove_buttons) > 0:
                remove_buttons[0].click()
                time.sleep(2)
                print("[CART-OPS] Item removed from cart")
        
        print("[CART-OPS] Cart operations test completed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()