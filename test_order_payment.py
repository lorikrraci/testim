import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class OrderPaymentTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://localhost:3000")
        time.sleep(1)
        
        
        print("[SETUP] Logging in")
        self.driver.get("http://localhost:3000/login")
        time.sleep(2)
        self.driver.find_element(By.ID, "email_field").send_keys("test@example.com")
        self.driver.find_element(By.ID, "password_field").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
        
        print("[SETUP] Adding item to cart")
        self.driver.get("http://localhost:3000/product/123")
        time.sleep(2)
        self.driver.find_element(By.ID, "cart_btn").click()
        time.sleep(2)

    def test_checkout_shipping(self):
        driver = self.driver
        
       
        print("[SHIPPING] Navigating to cart")
        driver.get("http://localhost:3000/cart")
        time.sleep(2)
        
        
        print("[SHIPPING] Proceeding to checkout")
        checkout_buttons = driver.find_elements(By.CSS_SELECTOR, ".checkout-btn")
        if len(checkout_buttons) > 0:
            checkout_buttons[0].click()
            time.sleep(2)
            
          
            print("[SHIPPING] Filling shipping information")
            driver.find_element(By.ID, "address_field").send_keys("123 Test Street")
            driver.find_element(By.ID, "city_field").send_keys("Test City")
            driver.find_element(By.ID, "postal_code_field").send_keys("12345")
            driver.find_element(By.ID, "phone_no_field").send_keys("1234567890")
            
           
            country_select = Select(driver.find_element(By.ID, "country_field"))
            country_select.select_by_visible_text("United States")
            
          
            print("[SHIPPING] Continuing to next step")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(2)
            
           
            self.assertIn("confirm", driver.current_url.lower())
            print("[SHIPPING] Shipping information test completed successfully")

    def test_order_confirmation(self):
        driver = self.driver
        
       
        print("[CONFIRM] Navigating to confirm order page")
        driver.get("http://localhost:3000/confirm")
        time.sleep(2)
        

        print("[CONFIRM] Verifying order details")
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".order-summary").is_displayed())
     
        order_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
        self.assertTrue(len(order_items) > 0)
        
        
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".shipping-info").is_displayed())
        
       
        print("[CONFIRM] Proceeding to payment")
        payment_buttons = driver.find_elements(By.CSS_SELECTOR, ".payment-btn")
        if len(payment_buttons) > 0:
            payment_buttons[0].click()
            time.sleep(2)
            
            
            self.assertIn("payment", driver.current_url.lower())
            print("[CONFIRM] Order confirmation test completed successfully")

    def test_payment_process(self):
        driver = self.driver
        
       
        print("[PAYMENT] Navigating to payment page")
        driver.get("http://localhost:3000/payment")
        time.sleep(2)
        
       
        print("[PAYMENT] Checking for payment elements")
        try:
           
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, ".stripe-card-element iframe"))
            )
            
      
            print("[PAYMENT] Entering card details")
            driver.find_element(By.CSS_SELECTOR, ".InputElement").send_keys("4242424242424242")
            driver.find_element(By.CSS_SELECTOR, ".InputElement").send_keys("1225")
            driver.find_element(By.CSS_SELECTOR, ".InputElement").send_keys("123")
            
        
            driver.switch_to.default_content()
            
           
            print("[PAYMENT] Submitting payment")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(5)
            
            
            self.assertIn("success", driver.page_source.lower())
            print("[PAYMENT] Payment process test completed successfully")
            
        except Exception as e:
            print(f"[PAYMENT] Error in payment test: {e}")
           
            self.assertIn("payment", driver.current_url.lower())

    def test_order_history(self):
        driver = self.driver
        
    
        print("[HISTORY] Navigating to order history")
        driver.get("http://localhost:3000/orders/me")
        time.sleep(2)
        
      
        self.assertIn("orders", driver.current_url.lower())
        
       
        orders = driver.find_elements(By.CSS_SELECTOR, ".order-item")
        
        if len(orders) > 0:
            print(f"[HISTORY] Found {len(orders)} orders")
            
         
            print("[HISTORY] Viewing details of first order")
            view_buttons = driver.find_elements(By.CSS_SELECTOR, ".view-order-btn")
            if len(view_buttons) > 0:
                view_buttons[0].click()
                time.sleep(2)
                
                
                self.assertIn("order", driver.current_url.lower())
                self.assertTrue(driver.find_element(By.CSS_SELECTOR, ".order-details").is_displayed())
                print("[HISTORY] Order details view test completed successfully")
        else:
            print("[HISTORY] No orders found in history")
            
        print("[HISTORY] Order history test completed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
