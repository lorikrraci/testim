import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserAccountTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("http://localhost:3000")
        time.sleep(1)

    def test_user_registration(self):
        driver = self.driver
        
      
        print("[REGISTER] Navigating to registration page")
        driver.get("http://localhost:3000/register")
        time.sleep(2)
        
        
        random_num = random.randint(1000, 9999)
        name = f"Test User {random_num}"
        email = f"testuser{random_num}@example.com"
        password = "Test@123456"
        
        
        print(f"[REGISTER] Filling form with name={name}, email={email}")
        driver.find_element(By.ID, "name_field").send_keys(name)
        driver.find_element(By.ID, "email_field").send_keys(email)
        driver.find_element(By.ID, "password_field").send_keys(password)
        
      
        print("[REGISTER] Submitting registration form")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
       
        self.assertIn("registered", driver.page_source.lower())
        print("[REGISTER] Registration test completed successfully")

    def test_user_login(self):
        driver = self.driver
        
     
        print("[LOGIN] Navigating to login page")
        driver.get("http://localhost:3000/login")
        time.sleep(2)
        
    
        print("[LOGIN] Entering credentials")
        driver.find_element(By.ID, "email_field").send_keys("test@example.com")
        driver.find_element(By.ID, "password_field").send_keys("password123")
        
       
        print("[LOGIN] Submitting login form")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
        
        self.assertTrue(
            driver.find_element(By.CSS_SELECTOR, ".dropdown-toggle").is_displayed()
        )
        print("[LOGIN] Login test completed successfully")

    def test_update_profile(self):
        driver = self.driver
        
      
        print("[PROFILE] Logging in first")
        driver.get("http://localhost:3000/login")
        time.sleep(2)
        driver.find_element(By.ID, "email_field").send_keys("test@example.com")
        driver.find_element(By.ID, "password_field").send_keys("password123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
    
        print("[PROFILE] Navigating to profile page")
        driver.get("http://localhost:3000/me/update")
        time.sleep(2)
        
     
        print("[PROFILE] Updating profile information")
        name_field = driver.find_element(By.ID, "name_field")
        name_field.clear()
        name_field.send_keys("Updated Test User")
        
       
        print("[PROFILE] Submitting updated profile")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        

        self.assertIn("updated", driver.page_source.lower())
        print("[PROFILE] Profile update test completed successfully")

    def test_password_reset(self):
        driver = self.driver
        
        
        print("[PASSWORD] Navigating to password reset page")
        driver.get("http://localhost:3000/password/forgot")
        time.sleep(2)
        
       
        print("[PASSWORD] Entering email for password reset")
        driver.find_element(By.ID, "email_field").send_keys("test@example.com")
        
       
        print("[PASSWORD] Submitting password reset request")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        
       
        self.assertIn("email", driver.page_source.lower())
        self.assertIn("sent", driver.page_source.lower())
        print("[PASSWORD] Password reset test completed successfully")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()