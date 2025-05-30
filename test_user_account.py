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
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Setup WebDriver with ChromeDriverManager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        
        # Base URL - change if your app runs on a different port
        self.base_url = "http://localhost:3000"
        self.driver.get(self.base_url)
        
        # Wait for page to load
        self.wait = WebDriverWait(self.driver, 15)
        print(f"[SETUP] Browser initialized and navigated to {self.base_url}")
        
        # Take screenshot of homepage
        self.take_screenshot("homepage")
        
        # Connect to MongoDB and get a test user
        try:
            # Connect to MongoDB - update connection string as needed
            client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
            db = client["shopit"]  # Use your actual database name
            users_collection = db["users"]  # Use your actual collection name
            
            # Find a user with role "user" (not admin)
            user_doc = users_collection.find_one({"role": "user"})
            
            if user_doc:
                self.test_user = {
                    "name": user_doc.get("name", "Test User"),
                    "email": user_doc.get("email", "test@example.com"),
                    "password": "password123"  # Note: You won't have the actual password in the DB
                }
                print(f"[SETUP] Found test user in database: {self.test_user['email']}")
            else:
                # Generate random test user if none found
                self.random_num = random.randint(1000, 9999)
                self.test_user = {
                    "name": f"Test User {self.random_num}",
                    "email": f"testuser{self.random_num}@example.com",
                    "password": "Test@123456"
                }
                print(f"[SETUP] Generated test user: {self.test_user['name']}, {self.test_user['email']}")
        except Exception as e:
            print(f"[SETUP] Error connecting to database: {str(e)}")
            # Generate random test user as fallback
            self.random_num = random.randint(1000, 9999)
            self.test_user = {
                "name": f"Test User {self.random_num}",
                "email": f"testuser{self.random_num}@example.com",
                "password": "Test@123456"
            }
            print(f"[SETUP] Generated test user: {self.test_user['name']}, {self.test_user['email']}")

    def take_screenshot(self, name):
        """Helper method to take screenshots for debugging"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{name}.png")
        print(f"[INFO] Screenshot saved: screenshots/{name}.png")

    def find_element_with_multiple_strategies(self, strategies):
        """Try multiple strategies to find an element"""
        for strategy in strategies:
            by, value = strategy
            try:
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                print(f"[INFO] Found element using {by}={value}")
                return element
            except (TimeoutException, NoSuchElementException):
                print(f"[INFO] Could not find element using {by}={value}")
                continue
        
        # If we get here, all strategies failed
        self.take_screenshot("element_not_found")
        raise NoSuchElementException(f"Could not find element using any of the strategies: {strategies}")

    def test_1_user_registration(self):
        """Test user registration with a new account"""
        driver = self.driver
        
        try:
            print("[REGISTER] Navigating to registration page")
            driver.get(f"{self.base_url}/register")
            time.sleep(2)
            self.take_screenshot("register_page")
            
            print(f"[REGISTER] Filling form with name={self.test_user['name']}, email={self.test_user['email']}")
            
            # Find name field
            name_field = self.find_element_with_multiple_strategies([
                (By.ID, "name"),
                (By.NAME, "name"),
                (By.CSS_SELECTOR, "input[placeholder*='name' i]"),
                (By.CSS_SELECTOR, "input[type='text']")
            ])
            name_field.clear()
            name_field.send_keys(self.test_user['name'])
            
            # Find email field
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            # Find password field
            password_field = self.find_element_with_multiple_strategies([
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ])
            password_field.clear()
            password_field.send_keys(self.test_user['password'])
            
            # Take screenshot before submitting
            self.take_screenshot("register_form_filled")
            
            print("[REGISTER] Submitting registration form")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Register')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            # Wait for registration to complete
            time.sleep(5)
            self.take_screenshot("after_registration")
            
            # Check for success
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["registered", "success", "welcome", "account", "profile"])
            
            self.assertTrue(success, "Registration success indicator not found")
            print("[REGISTER] Registration test completed successfully")
            
            # Save user credentials to a file for reference
            with open("test_user_credentials.txt", "w") as f:
                f.write(f"Name: {self.test_user['name']}\n")
                f.write(f"Email: {self.test_user['email']}\n")
                f.write(f"Password: {self.test_user['password']}\n")
            
        except Exception as e:
            self.take_screenshot("register_error")
            self.fail(f"Registration test failed: {str(e)}")

    def test_user_login(self):
        """Test login with the newly registered account"""
        driver = self.driver
        
        try:
            print("[LOGIN] Navigating to login page")
            driver.get(f"{self.base_url}/login")
            time.sleep(2)
            self.take_screenshot("login_page")
            
            print(f"[LOGIN] Entering credentials for {self.test_user['email']}")
            # Find email field
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            # Find password field
            password_field = self.find_element_with_multiple_strategies([
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ])
            password_field.clear()
            password_field.send_keys(self.test_user['password'])
            
            # Take screenshot before submitting
            self.take_screenshot("login_form_filled")
            
            print("[LOGIN] Submitting login form")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            self.take_screenshot("after_login")
            
            # Check for success
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["logout", "profile", "account", "dashboard"])
            
            self.assertTrue(success, "Login success indicator not found")
            print("[LOGIN] Login test completed successfully")
            
        except Exception as e:
            self.take_screenshot("login_error")
            self.fail(f"Login test failed: {str(e)}")

    def test_3_update_profile(self):
        """Test updating profile after login"""
        driver = self.driver
        
        try:
            # Login first using our test user
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
            
            # Navigate to profile page - try different possible URLs
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
                    # Check if we're on a profile page by looking for a name field
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
            # Find name field
            name_field = self.find_element_with_multiple_strategies([
                (By.ID, "name"),
                (By.NAME, "name"),
                (By.CSS_SELECTOR, "input[placeholder*='name' i]")
            ])
            name_field.clear()
            updated_name = f"Updated {self.test_user['name']}"
            name_field.send_keys(updated_name)
            
            # Take screenshot before submitting
            self.take_screenshot("profile_form_filled")
            
            print("[PROFILE] Submitting updated profile")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Update')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            # Wait for update to complete
            time.sleep(5)
            self.take_screenshot("after_profile_update")
            
            # Check for success
            page_source = driver.page_source.lower()
            success = any(word in page_source for word in ["updated", "success", "profile"])
            
            self.assertTrue(success, "Profile update success indicator not found")
            print("[PROFILE] Profile update test completed successfully")
            
            # Update our test user data
            self.test_user['name'] = updated_name
            
        except Exception as e:
            self.take_screenshot("profile_update_error")
            self.fail(f"Profile update test failed: {str(e)}")

    def test_4_password_reset(self):
        """Test password reset functionality"""
        driver = self.driver
        
        try:
            # Try different possible URLs for password reset
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
                    # Check if we're on a password reset page by looking for an email field
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
            # Find email field
            email_field = self.find_element_with_multiple_strategies([
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]")
            ])
            email_field.clear()
            email_field.send_keys(self.test_user['email'])
            
            # Take screenshot before submitting
            self.take_screenshot("password_reset_form_filled")
            
            print("[PASSWORD] Submitting password reset request")
            submit_button = self.find_element_with_multiple_strategies([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Reset')]"),
                (By.XPATH, "//button[contains(text(), 'Send')]"),
                (By.XPATH, "//input[@type='submit']")
            ])
            submit_button.click()
            
            # Wait for request to complete
            time.sleep(5)
            self.take_screenshot("after_password_reset")
            
            # Check for success
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
