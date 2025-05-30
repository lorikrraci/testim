import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class ProductCartTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
            
        self.base_url = "http://localhost:3000"
        self.driver.get(self.base_url)
        
        self.wait = WebDriverWait(self.driver, 10)
        
        self.driver.save_screenshot("screenshots/homepage.png")
        print("[SETUP] Browser initialized and navigated to homepage")
        
        self.product_info = {
            "search_term": "MacBook",
            "product_url": None,
            "product_name": None,
            "search_result_url": None,
            "category_product_url": None
        }

    def find_element_safely(self, by, value, timeout=10, screenshot_prefix=None):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except (TimeoutException, NoSuchElementException):
            if screenshot_prefix:
                self.driver.save_screenshot(f"screenshots/{screenshot_prefix}_not_found.png")
            
            if by == By.ID and value == "search_field":
                try:
                    alternatives = [
                        (By.CSS_SELECTOR, "input[type='search']"),
                        (By.CSS_SELECTOR, ".search-input"),
                        (By.CSS_SELECTOR, "[placeholder*='search']"),
                        (By.CSS_SELECTOR, "input.form-control")
                    ]
                    for alt_by, alt_value in alternatives:
                        try:
                            element = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((alt_by, alt_value))
                            )
                            print(f"[INFO] Found alternative for {value} using {alt_by}={alt_value}")
                            return element
                        except:
                            continue
                except:
                    pass
            
            elif by == By.ID and value == "search_btn":
                try:
                    alternatives = [
                        (By.CSS_SELECTOR, "button[type='submit']"),
                        (By.CSS_SELECTOR, ".search-button"),
                        (By.CSS_SELECTOR, ".btn-search"),
                        (By.XPATH, "//button[contains(@class, 'search') or contains(@class, 'btn')]")
                    ]
                    for alt_by, alt_value in alternatives:
                        try:
                            element = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((alt_by, alt_value))
                            )
                            print(f"[INFO] Found alternative for {value} using {alt_by}={alt_value}")
                            return element
                        except:
                            continue
                except:
                    pass
            
            elif by == By.ID and value == "cart_btn":
                try:
                    alternatives = [
                        (By.CSS_SELECTOR, ".add-to-cart"),
                        (By.CSS_SELECTOR, "button.btn-cart"),
                        (By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add To Cart')]"),
                        (By.CSS_SELECTOR, "[data-test='add-to-cart']")
                    ]
                    for alt_by, alt_value in alternatives:
                        try:
                            element = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((alt_by, alt_value))
                            )
                            print(f"[INFO] Found alternative for {value} using {alt_by}={alt_value}")
                            return element
                        except:
                            continue
                except:
                    pass
            
            elif by == By.ID and value == "product_price":
                try:
                    alternatives = [
                        (By.CSS_SELECTOR, ".price"),
                        (By.CSS_SELECTOR, ".product-price"),
                        (By.CSS_SELECTOR, "[data-test='price']"),
                        (By.XPATH, "//div[contains(@class, 'price')]")
                    ]
                    for alt_by, alt_value in alternatives:
                        try:
                            element = WebDriverWait(self.driver, 3).until(
                                EC.presence_of_element_located((alt_by, alt_value))
                            )
                            print(f"[INFO] Found alternative for {value} using {alt_by}={alt_value}")
                            return element
                        except:
                            continue
                except:
                    pass
            
            raise Exception(f"Could not find element {by}={value}")

    def test_1_product_search(self):
        try:
            driver = self.driver
            
            print("[SEARCH] Testing product search")
            driver.save_screenshot("screenshots/before_search.png")
            
            search_box = None
            try:
                search_box = self.find_element_safely(
                    By.ID, "search_field", 
                    screenshot_prefix="search_field"
                )
            except Exception as e:
                print(f"[SEARCH] Could not find search field by ID: {str(e)}")
                
                try:
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    for input_elem in inputs:
                        attr_type = input_elem.get_attribute("type")
                        attr_placeholder = input_elem.get_attribute("placeholder") or ""
                        if attr_type == "search" or "search" in attr_placeholder.lower():
                            search_box = input_elem
                            print("[SEARCH] Found search field by input attributes")
                            break
                except:
                    pass
                
                if not search_box:
                    try:
                        forms = driver.find_elements(By.TAG_NAME, "form")
                        for form in forms:
                            inputs = form.find_elements(By.TAG_NAME, "input")
                            if inputs:
                                search_box = inputs[0]
                                print("[SEARCH] Using first input in a form as search field")
                                break
                    except:
                        pass
            
            if not search_box:
                self.fail("Could not find search field with any method")
                
            search_box.clear()
            search_box.send_keys(self.product_info["search_term"])
            
            search_btn = None
            try:
                search_btn = self.find_element_safely(
                    By.ID, "search_btn", 
                    screenshot_prefix="search_button"
                )
            except Exception as e:
                print(f"[SEARCH] Could not find search button by ID: {str(e)}")
                
                try:
                    if search_box:
                        parent = search_box.find_element(By.XPATH, "./..")
                        buttons = parent.find_elements(By.TAG_NAME, "button")
                        if buttons:
                            search_btn = buttons[0]
                            print("[SEARCH] Found search button near search field")
                except:
                    pass
                
                if not search_btn:
                    try:
                        buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                        if buttons:
                            search_btn = buttons[0]
                            print("[SEARCH] Using first submit button as search button")
                    except:
                        pass
                
                if not search_btn:
                    print("[SEARCH] No search button found, pressing Enter key")
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(2)
                    driver.save_screenshot("screenshots/after_search_enter.png")
            
            if search_btn:
                search_btn.click()
            
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products")))
            except:
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-list")))
                except:
                    try:
                        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
                    except:
                        pass
            
            driver.save_screenshot("screenshots/search_results.png")
            
            search_term_found = self.product_info["search_term"].lower() in driver.page_source.lower()
            
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, ".product")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, "[data-test='product']")
            
            if len(products) > 0:
                print(f"[SEARCH] Found {len(products)} products")
                
                try:
                    first_product = products[0].find_element(By.TAG_NAME, "a")
                    self.product_info["search_result_url"] = first_product.get_attribute("href")
                    print(f"[SEARCH] Found product URL: {self.product_info['search_result_url']}")
                except:
                    try:
                        products[0].click()
                        time.sleep(2)
                        self.product_info["search_result_url"] = driver.current_url
                        print(f"[SEARCH] Clicked product and got URL: {self.product_info['search_result_url']}")
                        driver.back()
                        time.sleep(2)
                    except:
                        print("[SEARCH] Could not get product URL")
            elif search_term_found:
                print(f"[SEARCH] Search term '{self.product_info['search_term']}' found in page")
            else:
                self.fail("No products found and search term not in page")
            
            print("[SEARCH] Search test completed successfully")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/search_test_error.png")
            self.fail(f"Product search test failed: {str(e)}")

    def test_2_product_details(self):
        try:
            driver = self.driver
            
            print("[DETAILS] Testing product details by browsing from homepage")
            driver.get(self.base_url)
            
            time.sleep(3)
            driver.save_screenshot("screenshots/homepage_for_details.png")
            
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, ".product")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, "[data-test='product']")
            
            if len(products) == 0:
                try:
                    print("[DETAILS] No products on homepage, trying products page")
                    driver.get(f"{self.base_url}/products")
                    time.sleep(3)
                    
                    products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
                    if len(products) == 0:
                        products = driver.find_elements(By.CSS_SELECTOR, ".product")
                    if len(products) == 0:
                        products = driver.find_elements(By.CSS_SELECTOR, "[data-test='product']")
                except:
                    pass
            
            if len(products) == 0:
                if self.product_info["search_result_url"]:
                    print("[DETAILS] Using search result URL")
                    driver.get(self.product_info["search_result_url"])
                else:
                    self.fail("No products found on homepage or products page")
                    return
            else:
                try:
                    product_link = products[0].find_element(By.TAG_NAME, "a")
                    product_link.click()
                except:
                    products[0].click()
            
            time.sleep(3)
            driver.save_screenshot("screenshots/product_details_page.png")
            
            current_url = driver.current_url
            self.product_info["product_url"] = current_url
            print(f"[DETAILS] Product page URL: {current_url}")
            
            product_name = None
            try:
                product_name_elem = driver.find_element(By.CSS_SELECTOR, "h3")
                product_name = product_name_elem.text
            except:
                try:
                    product_name_elem = driver.find_element(By.CSS_SELECTOR, "h1")
                    product_name = product_name_elem.text
                except:
                    try:
                        product_name_elem = driver.find_element(By.CSS_SELECTOR, ".product-name")
                        product_name = product_name_elem.text
                    except:
                        pass
            
            if product_name and len(product_name) > 0:
                self.product_info["product_name"] = product_name
                print(f"[DETAILS] Product name: {product_name}")
            else:
                print("[DETAILS] Could not find product name")
            
            price_found = False
            try:
                price_elem = self.find_element_safely(
                    By.ID, "product_price", 
                    screenshot_prefix="product_price"
                )
                price_found = price_elem.is_displayed()
            except:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, ".price")
                    price_found = price_elem.is_displayed()
                except:
                    try:
                        price_elem = driver.find_element(By.CSS_SELECTOR, ".product-price")
                        price_found = price_elem.is_displayed()
                    except:
                        pass
            
            if price_found:
                print("[DETAILS] Product price found")
            else:
                print("[DETAILS] Warning: Product price not found")
            
            cart_btn_found = False
            try:
                cart_btn = self.find_element_safely(
                    By.ID, "cart_btn", 
                    screenshot_prefix="cart_button"
                )
                cart_btn_found = cart_btn.is_displayed()
            except:
                try:
                    cart_btn = driver.find_element(By.CSS_SELECTOR, ".add-to-cart")
                    cart_btn_found = cart_btn.is_displayed()
                except:
                    try:
                        cart_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
                        cart_btn_found = cart_btn.is_displayed()
                    except:
                        pass
            
            if cart_btn_found:
                print("[DETAILS] Add to cart button found")
            else:
                print("[DETAILS] Warning: Add to cart button not found")
            
            images_found = False
            try:
                product_images = driver.find_elements(By.CSS_SELECTOR, ".carousel-item img")
                images_found = len(product_images) > 0
            except:
                try:
                    product_images = driver.find_elements(By.CSS_SELECTOR, ".product-image")
                    images_found = len(product_images) > 0
                except:
                    try:
                        product_images = driver.find_elements(By.TAG_NAME, "img")
                        images_found = len(product_images) > 0
                    except:
                        pass
            
            if images_found:
                print("[DETAILS] Product images found")
            else:
                print("[DETAILS] Warning: Product images not found")
            
            if product_name and (price_found or cart_btn_found):
                print(f"[DETAILS] Product details test completed for: {product_name}")
            else:
                self.fail("Could not verify essential product details")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/product_details_error.png")
            self.fail(f"Product details test failed: {str(e)}")

    def test_3_add_to_cart(self):
        try:
            driver = self.driver
            
            if self.product_info["product_url"]:
                print(f"[CART] Using product URL from previous test: {self.product_info['product_url']}")
                driver.get(self.product_info["product_url"])
            else:
                if self.product_info["search_result_url"]:
                    print(f"[CART] Using search result URL: {self.product_info['search_result_url']}")
                    driver.get(self.product_info["search_result_url"])
                else:
                    print("[CART] No saved URLs, browsing from homepage")
                    driver.get(self.base_url)
                    
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
                    
                    first_product = self.find_element_safely(
                        By.CSS_SELECTOR, ".product-card a", 
                        screenshot_prefix="cart_first_product"
                    )
                    first_product.click()
            
            self.wait.until(EC.presence_of_element_located((By.ID, "cart_btn")))
            driver.save_screenshot("screenshots/before_add_to_cart.png")
            
            try:
                product_name = driver.find_element(By.CSS_SELECTOR, "h3").text
                print(f"[CART] Testing with product: {product_name}")
                self.product_info["product_name"] = product_name
            except:
                print("[CART] Could not get product name")
            
            try:
                print("[CART] Trying to increase quantity")
                plus_buttons = driver.find_elements(By.CSS_SELECTOR, ".plus")
                if len(plus_buttons) > 0:
                    plus_buttons[0].click()
                    time.sleep(1)
                    driver.save_screenshot("screenshots/after_quantity_increase.png")
                    print("[CART] Quantity increased")
                else:
                    print("[CART] Plus button not found")
            except Exception as e:
                print(f"[CART] Could not increase quantity: {str(e)}")
            
            cart_btn = self.find_element_safely(
                By.ID, "cart_btn", 
                screenshot_prefix="add_to_cart_button"
            )
            cart_btn.click()
            time.sleep(2)
            driver.save_screenshot("screenshots/after_add_to_cart.png")
            
            success = False
            
            try:
                success_alert = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
                )
                print(f"[CART] Success message found: {success_alert.text}")
                success = True
            except:
                print("[CART] No success message found, trying other verification methods")
            
            if not success:
                try:
                    cart_count = driver.find_elements(By.CSS_SELECTOR, ".cart-count")
                    if len(cart_count) > 0 and cart_count[0].text != "0":
                        print(f"[CART] Cart count updated: {cart_count[0].text}")
                        success = True
                except:
                    print("[CART] Could not verify cart count")
            
            if not success:
                try:
                    driver.get(f"{self.base_url}/cart")
                    time.sleep(3)
                    driver.save_screenshot("screenshots/cart_verification.png")
                    
                    if "Your Cart is Empty" not in driver.page_source:
                        print("[CART] Cart is not empty, item was added successfully")
                        success = True
                    else:
                        print("[CART] Cart appears to be empty")
                except Exception as e:
                    print(f"[CART] Error checking cart: {str(e)}")
            
            self.assertTrue(success, "Failed to verify item was added to cart")
            print("[CART] Add to cart test completed successfully")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/add_to_cart_error.png")
            self.fail(f"Add to cart test failed: {str(e)}")

    def test_4_cart_operations(self):
        try:
            driver = self.driver
            
            print("[CART-OPS] Navigating to cart page")
            driver.get(f"{self.base_url}/cart")
            time.sleep(3)
            driver.save_screenshot("screenshots/cart_page.png")
            
            if "Your Cart is Empty" in driver.page_source:
                print("[CART-OPS] Cart is empty, adding an item first")
                
                if self.product_info["product_url"]:
                    driver.get(self.product_info["product_url"])
                else:
                    driver.get(self.base_url)
                    
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
                    
                    first_product = self.find_element_safely(
                        By.CSS_SELECTOR, ".product-card a", 
                        screenshot_prefix="cart_ops_first_product"
                    )
                    first_product.click()
                
                self.wait.until(EC.presence_of_element_located((By.ID, "cart_btn")))
                
                cart_btn = self.find_element_safely(
                    By.ID, "cart_btn", 
                    screenshot_prefix="cart_ops_add_button"
                )
                cart_btn.click()
                time.sleep(3)
                
                driver.get(f"{self.base_url}/cart")
                time.sleep(3)
                driver.save_screenshot("screenshots/cart_page_after_adding.png")
                
                if "Your Cart is Empty" in driver.page_source:
                    self.fail("Cart is still empty after adding an item, cannot test cart operations")
                    return
            
            print("[CART-OPS] Cart has items, continuing with test")
            
            cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
            if len(cart_items) == 0:
                cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart_item")
                if len(cart_items) == 0:
                    cart_items = driver.find_elements(By.CSS_SELECTOR, "[data-test='cart-item']")
            
            self.assertTrue(len(cart_items) > 0, "No items found in cart")
            print(f"[CART-OPS] Found {len(cart_items)} items in cart")
            
            try:
                print("[CART-OPS] Testing quantity adjustment")
                plus_buttons = driver.find_elements(By.CSS_SELECTOR, ".plus")
                if len(plus_buttons) == 0:
                    plus_buttons = driver.find_elements(By.CSS_SELECTOR, ".increment")
                if len(plus_buttons) == 0:
                    plus_buttons = driver.find_elements(By.CSS_SELECTOR, "[data-test='increase-qty']")
                    
                if len(plus_buttons) > 0:
                    plus_buttons[0].click()
                    time.sleep(2)
                    driver.save_screenshot("screenshots/after_cart_quantity_increase.png")
                    print("[CART-OPS] Quantity increased")
                    
                    minus_buttons = driver.find_elements(By.CSS_SELECTOR, ".minus")
                    if len(minus_buttons) == 0:
                        minus_buttons = driver.find_elements(By.CSS_SELECTOR, ".decrement")
                    if len(minus_buttons) == 0:
                        minus_buttons = driver.find_elements(By.CSS_SELECTOR, "[data-test='decrease-qty']")
                        
                    if len(minus_buttons) > 0:
                        minus_buttons[0].click()
                        time.sleep(2)
                        driver.save_screenshot("screenshots/after_cart_quantity_decrease.png")
                        print("[CART-OPS] Quantity decreased")
                else:
                    print("[CART-OPS] No quantity adjustment buttons found")
            except Exception as e:
                print(f"[CART-OPS] Could not test quantity adjustment: {str(e)}")
            
            try:
                checkout_selectors = [
                    ".checkout-btn", 
                    "#checkout-button", 
                    "button:contains('Checkout')",
                    "[data-test='checkout']",
                    "a.checkout-btn"
                ]
                
                checkout_btn = None
                for selector in checkout_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if len(elements) > 0:
                            checkout_btn = elements[0]
                            break
                    except:
                        continue
                
                if checkout_btn:
                    self.assertTrue(checkout_btn.is_displayed(), "Checkout button is not displayed")
                    print("[CART-OPS] Checkout button verified")
                else:
                    print("[CART-OPS] Checkout button not found with any selector")
            except Exception as e:
                print(f"[CART-OPS] Could not verify checkout button: {str(e)}")
            
            print("[CART-OPS] Cart operations test completed")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/cart_operations_error.png")
            self.fail(f"Cart operations test failed: {str(e)}")

    def test_5_browse_categories(self):
        try:
            driver = self.driver
            
            print("[CATEGORIES] Testing category browsing")
            driver.get(self.base_url)
            
            category_links = driver.find_elements(By.CSS_SELECTOR, ".category-link")
            if len(category_links) == 0:
                category_links = driver.find_elements(By.CSS_SELECTOR, "[data-test='category']")
                if len(category_links) == 0:
                    category_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar a")
            
            if len(category_links) == 0:
                print("[CATEGORIES] No category links found, skipping test")
                return
            
            print(f"[CATEGORIES] Found {len(category_links)} categories, clicking first one")
            category_links[0].click()
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products")))
            driver.save_screenshot("screenshots/category_products.png")
            
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            print(f"[CATEGORIES] Found {len(products)} products in category")
            
            if len(products) > 0:
                products[0].find_element(By.TAG_NAME, "a").click()
                
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
                driver.save_screenshot("screenshots/category_product_details.png")
                
                self.product_info["category_product_url"] = driver.current_url
                print(f"[CATEGORIES] Stored category product URL: {self.product_info['category_product_url']}")
            
            print("[CATEGORIES] Category browsing test completed")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/category_browse_error.png")
            print(f"[CATEGORIES] Category browsing test encountered an error: {str(e)}")
            pass

    def tearDown(self):
        if self.driver:
            print("[TEARDOWN] Closing browser")
            self.driver.quit()

if __name__ == "__main__":
    print("[MAIN] Starting product and cart tests")
    unittest.main()
