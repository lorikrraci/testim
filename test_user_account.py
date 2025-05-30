import unittest
import time
import random
import os
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class UserAccountTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        
        self.base_url = "http://localhost:3000"
        self.driver.get(self.base_url)
        
        self.wait = WebDriverWait(self.driver, 15)
        print(f"[SETUP] Browser initialized and navigated to {self.base_url}")
        
        self.take_screenshot("homepage")
        
        try:
            client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
            db = client["shopit"]  
            users_collection = db["users"]  
            
            user_doc = users_collection.find_one({"role": "user"})
            
            if user_doc:
                self.test_user = {
                    "name": user_doc.get("name", "Test User"),
                    "email": user_doc.get("email", "test@example.com"),
                    "password": "password123"  
                }
                print(f"[SETUP] Found test user in database: {self.test_user['email']}")
            else:
                self.random_num = random.randint(1000, 9999)
                self.test_user = {
                    "name": f"Test User {self.random_num}",
                    "email": f"testuser{self.random_num}@example.com",
                    "password": "Test@123456"
                }
                print(f"[SETUP] Generated test user: {self.test_user['name']}, {self.test_user['email']}")
        except Exception as e:
            print(f"[SETUP] Error connecting to database: {str(e)}")
            self.random_num = random.randint(1000, 9999)
            self.test_user = {
                "name": f"Test User {self.random_num}",
                "email": f"testuser{self.random_num}@example.com",
                "password": "Test@123456"
            }
            print(f"[SETUP] Generated test user: {self.test_user['name']}, {self.test_user['email']}")

    def take_screenshot(self, name):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{name}.png")
        print(f"[INFO] Screenshot saved: screenshots/{name}.png")

    def find_element_with_multiple_strategies(self, strategies):
        for strategy in strategies:
            by, value = strategy
            try:
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                print(f"[INFO] Found element using {by}={value}")
                return element
            except (TimeoutException, NoSuchElementException):
                print(f"[INFO] Could not find element using {by}={value}")
                continue
        
        self.take_screenshot("element_not_found")
        raise NoSuchElementException(f"Could not find element using any of the strategies: {strategies}")

    def test_1_user_registration(self):
        driver = self.driver
        
        try:
            print("[REGISTER] Navigating to registration page")
            driver.get(f"{self.base_url}/register")
            time.sleep(2)
            self.take_screenshot("register_page")
            
            print(f"[REGISTER] Filling form with name={self.test_user['name']}, email={self.test_user['email']}")
            
            name_field = self.find_element_with_multiple_strategies([
                (By.ID, "name"),
                (By.NAME, "name"),
                (By.CSS_SELECTOR, "input[placeholder*='name' i]"),
                (By.CSS_SELECTOR, "input[type='text']")
            ])
            name_field.clear()
            name_field.send_keys(self.test_user['name'])
            
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            password_field = self.find_element_with_multiple_strategies([
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ])
            password_field.clear()
            password_field.send_keys(self.test_user['password'])
            
            self.take_screenshot("register_form_filled")
            
            print("[REGISTER] Submitting registration form")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Register')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            time.sleep(5)
            self.take_screenshot("after_registration")
            
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["registered", "success", "welcome", "account", "profile"])
            
            self.assertTrue(success, "Registration success indicator not found")
            print("[REGISTER] Registration test completed successfully")
            
            with open("test_user_credentials.txt", "w") as f:
                f.write(f"Name: {self.test_user['name']}\n")
                f.write(f"Email: {self.test_user['email']}\n")
                f.write(f"Password: {self.test_user['password']}\n")
            
        except Exception as e:
            self.take_screenshot("register_error")
            self.fail(f"Registration test failed: {str(e)}")

    def test_user_login(self):
        driver = self.driver
        
        try:
            print("[LOGIN] Navigating to login page")
            driver.get(f"{self.base_url}/login")
            time.sleep(2)
            self.take_screenshot("login_page")
            
            print(f"[LOGIN] Entering credentials for {self.test_user['email']}")
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            password_field = self.find_element_with_multiple_strategies([
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ])
            password_field.clear()
            password_field.send_keys(self.test_user['password'])
            
            self.take_screenshot("login_form_filled")
            
            print("[LOGIN] Submitting login form")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            time.sleep(5)
            self.take_screenshot("after_login")
            
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["logout", "profile", "account", "dashboard"])
            
            self.assertTrue(success, "Login success indicator not found")
            print("[LOGIN] Login test completed successfully")
            
        except Exception as e:
            self.take_screenshot("login_error")
            self.fail(f"Login test failed: {str(e)}")

    def test_3_update_profile(self):
        driver = self.driver
        
        try:
            print("[PROFILE] Logging in first")
            driver.get(f"{self.base_url}/login")
            time.sleep(2)
            
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            password_field = self.find_element_with_multiple_strategies([
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ])
            password_field.clear()
            password_field.send_keys(self.test_user['password'])
            
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]")
            ])
            submit_button.click()
            time.sleep(3)
            
            print("[PROFILE] Navigating to profile page")
            profile_urls = [
                f"{self.base_url}/me/update",
                f"{self.base_url}/profile",
                f"{self.base_url}/account",
                f"{self.base_url}/me"
            ]
            
            for url in profile_urls:
                try:
                    driver.get(url)
                    time.sleep(2)
                    try:
                        self.find_element_with_multiple_strategies([
                            (By.ID, "name"),
                            (By.NAME, "name"),
                            (By.CSS_SELECTOR, "input[placeholder*='name' i]")
                        ])
                        print(f"[PROFILE] Found profile page at {url}")
                        self.take_screenshot("profile_page")
                        break
                    except:
                        print(f"[PROFILE] {url} does not appear to be a profile page")
                        continue
                except:
                    continue
            
            print("[PROFILE] Updating profile information")
            name_field = self.find_element_with_multiple_strategies([
                (By.ID, "name"),
                (By.NAME, "name"),
                (By.CSS_SELECTOR, "input[placeholder*='name' i]")
            ])
            name_field.clear()
            updated_name = f"Updated {self.test_user['name']}"
            name_field.send_keys(updated_name)
            
            self.take_screenshot("profile_form_filled")
            
            print("[PROFILE] Submitting updated profile")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Update')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            time.sleep(5)
            self.take_screenshot("after_profile_update")
            
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["updated", "success", "profile"])
            
            self.assertTrue(success, "Profile update success indicator not found")
            print("[PROFILE] Profile update test completed successfully")
            
            self.test_user['name'] = updated_name
            
        except Exception as e:
            self.take_screenshot("profile_update_error")
            self.fail(f"Profile update test failed: {str(e)}")

    def test_4_password_reset(self):
        driver = self.driver
        
        try:
            print("[PASSWORD] Navigating to password reset page")
            reset_urls = [
                f"{self.base_url}/password/forgot",
                f"{self.base_url}/forgot-password",
                f"{self.base_url}/reset-password",
                f"{self.base_url}/forgot"
            ]
            
            for url in reset_urls:
                try:
                    driver.get(url)
                    time.sleep(2)
                    try:
                        self.find_element_with_multiple_strategies([
                            (By.ID, "email"),
                            (By.NAME, "email"),
                            (By.CSS_SELECTOR, "input[type='email']")
                        ])
                        print(f"[PASSWORD] Found password reset page at {url}")
                        self.take_screenshot("password_reset_page")
                        break
                    except:
                        print(f"[PASSWORD] {url} does not appear to be a password reset page")
                        continue
                except:
                    continue
            
            print(f"[PASSWORD] Entering email for password reset: {self.test_user['email']}")
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            self.take_screenshot("password_reset_form_filled")
            
            print("[PASSWORD] Submitting password reset request")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Reset')]"),
                (By.XPATH, "//button[contains(text(), 'Send')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            time.sleep(5)
            self.take_screenshot("after_password_reset")
            
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["email", "sent", "reset", "success"])
            
            self.assertTrue(success, "Password reset success indicator not found")
            print("[PASSWORD] Password reset test completed successfully")
            
        except Exception as e:
            self.take_screenshot("password_reset_error")
            self.fail(f"Password reset test failed: {str(e)}")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
