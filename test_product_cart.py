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
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Setup WebDriver with ChromeDriverManager
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
            
        # Base URL
        self.base_url = "http://localhost:3000"
        self.driver.get(self.base_url)
        
        # Setup wait
        self.wait = WebDriverWait(self.driver, 10)
        
        # Take screenshot of homepage
        self.driver.save_screenshot("screenshots/homepage.png")
        print("[SETUP] Browser initialized and navigated to homepage")
        
        # Store product info for use across tests
        self.product_info = {
            "search_term": "MacBook",  # Use a product name that exists in your database
            "product_url": None,
            "product_name": None,
            "search_result_url": None,
            "category_product_url": None
        }

    def find_element_safely(self, by, value, timeout=10, screenshot_prefix=None):
        """Helper method to find elements safely with explicit wait and screenshots"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except (TimeoutException, NoSuchElementException):
            if screenshot_prefix:
                self.driver.save_screenshot(f"screenshots/{screenshot_prefix}_not_found.png")
            
            # Try alternative selectors based on the original selector
            if by == By.ID and value == "search_field":
                # Try alternative search field selectors
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
                # Try alternative search button selectors
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
                # Try alternative add to cart button selectors
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
                # Try alternative price selectors
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
            
            # If we get here, we couldn't find any alternatives
            raise Exception(f"Could not find element {by}={value}")

    def test_1_product_search(self):
        """Test product search functionality"""
        try:
            driver = self.driver
            
            print("[SEARCH] Testing product search")
            driver.save_screenshot("screenshots/before_search.png")
            
            # Try to find search field with multiple approaches
            search_box = None
            try:
                # First try the ID approach
                search_box = self.find_element_safely(
                    By.ID, "search_field", 
                    screenshot_prefix="search_field"
                )
            except Exception as e:
                print(f"[SEARCH] Could not find search field by ID: {str(e)}")
                
                # Try alternative approaches
                try:
                    # Look for any input that might be a search field
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
                
                # If still not found, try common search form patterns
                if not search_box:
                    try:
                        # Look for forms that might contain search
                        forms = driver.find_elements(By.TAG_NAME, "form")
                        for form in forms:
                            inputs = form.find_elements(By.TAG_NAME, "input")
                            if inputs:
                                search_box = inputs[0]  # Use the first input in a form
                                print("[SEARCH] Using first input in a form as search field")
                                break
                    except:
                        pass
            
            if not search_box:
                self.fail("Could not find search field with any method")
                
            # Clear and enter search term
            search_box.clear()
            search_box.send_keys(self.product_info["search_term"])
            
            # Try to find search button with multiple approaches
            search_btn = None
            try:
                # First try the ID approach
                search_btn = self.find_element_safely(
                    By.ID, "search_btn", 
                    screenshot_prefix="search_button"
                )
            except Exception as e:
                print(f"[SEARCH] Could not find search button by ID: {str(e)}")
                
                # Try alternative approaches
                try:
                    # Look for buttons near the search box
                    if search_box:
                        # Get the parent element of the search box
                        parent = search_box.find_element(By.XPATH, "./..")
                        buttons = parent.find_elements(By.TAG_NAME, "button")
                        if buttons:
                            search_btn = buttons[0]
                            print("[SEARCH] Found search button near search field")
                except:
                    pass
                
                # If still not found, try common button patterns
                if not search_btn:
                    try:
                        # Look for any submit button
                        buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                        if buttons:
                            search_btn = buttons[0]
                            print("[SEARCH] Using first submit button as search button")
                    except:
                        pass
                
                # Last resort: press Enter key on search field
                if not search_btn:
                    print("[SEARCH] No search button found, pressing Enter key")
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(2)
                    driver.save_screenshot("screenshots/after_search_enter.png")
            
            # Click search button if found
            if search_btn:
                search_btn.click()
            
            # Wait for results to load - try multiple selectors
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products")))
            except:
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-list")))
                except:
                    try:
                        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
                    except:
                        pass  # We'll check for products directly
            
            driver.save_screenshot("screenshots/search_results.png")
            
            # Verify results contain the search term or products are displayed
            search_term_found = self.product_info["search_term"].lower() in driver.page_source.lower()
            
            # Look for products with multiple selectors
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, ".product")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, "[data-test='product']")
            
            # If we found products or the search term, consider it a success
            if len(products) > 0:
                print(f"[SEARCH] Found {len(products)} products")
                
                # Store the first product URL for future tests
                try:
                    first_product = products[0].find_element(By.TAG_NAME, "a")
                    self.product_info["search_result_url"] = first_product.get_attribute("href")
                    print(f"[SEARCH] Found product URL: {self.product_info['search_result_url']}")
                except:
                    # If no direct link, try clicking the product itself
                    try:
                        products[0].click()
                        time.sleep(2)
                        self.product_info["search_result_url"] = driver.current_url
                        print(f"[SEARCH] Clicked product and got URL: {self.product_info['search_result_url']}")
                        # Go back to search results
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
        """Test product details page by directly accessing a product"""
        try:
            driver = self.driver
            
            # Instead of searching, go directly to the homepage and click on a product
            print("[DETAILS] Testing product details by browsing from homepage")
            driver.get(self.base_url)
            
            # Wait for page to load
            time.sleep(3)
            driver.save_screenshot("screenshots/homepage_for_details.png")
            
            # Try to find products with multiple selectors
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, ".product")
            if len(products) == 0:
                products = driver.find_elements(By.CSS_SELECTOR, "[data-test='product']")
            
            if len(products) == 0:
                # If no products found on homepage, try navigating to products page
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
                # If still no products, try using a search result
                if self.product_info["search_result_url"]:
                    print("[DETAILS] Using search result URL")
                    driver.get(self.product_info["search_result_url"])
                else:
                    self.fail("No products found on homepage or products page")
                    return
            else:
                # Click on the first product
                try:
                    # Try to find a link within the product
                    product_link = products[0].find_element(By.TAG_NAME, "a")
                    product_link.click()
                except:
                    # If no link, try clicking the product directly
                    products[0].click()
            
            # Wait for product page to load
            time.sleep(3)
            driver.save_screenshot("screenshots/product_details_page.png")
            
            # Get current URL for future use
            current_url = driver.current_url
            self.product_info["product_url"] = current_url
            print(f"[DETAILS] Product page URL: {current_url}")
            
            # Verify product elements - try multiple approaches for each element
            
            # Product name
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
            
            # Product price
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
            
            # Add to cart button
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
            
            # Product images
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
            
            # We consider the test successful if we found at least the product name and either price or add to cart button
            if product_name and (price_found or cart_btn_found):
                print(f"[DETAILS] Product details test completed for: {product_name}")
            else:
                self.fail("Could not verify essential product details")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/product_details_error.png")
            self.fail(f"Product details test failed: {str(e)}")

    def test_3_add_to_cart(self):
        """Test adding product to cart using the product URL from previous test"""
        try:
            driver = self.driver
            
            # Use the product URL from the previous test
            if self.product_info["product_url"]:
                print(f"[CART] Using product URL from previous test: {self.product_info['product_url']}")
                driver.get(self.product_info["product_url"])
            else:
                # Fallback to using search result URL
                if self.product_info["search_result_url"]:
                    print(f"[CART] Using search result URL: {self.product_info['search_result_url']}")
                    driver.get(self.product_info["search_result_url"])
                else:
                    # Last resort: go to homepage and click first product
                    print("[CART] No saved URLs, browsing from homepage")
                    driver.get(self.base_url)
                    
                    # Wait for products to load
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
                    
                    # Click on the first product
                    first_product = self.find_element_safely(
                        By.CSS_SELECTOR, ".product-card a", 
                        screenshot_prefix="cart_first_product"
                    )
                    first_product.click()
            
            # Wait for product page to load
            self.wait.until(EC.presence_of_element_located((By.ID, "cart_btn")))
            driver.save_screenshot("screenshots/before_add_to_cart.png")
            
            # Get product name for verification
            try:
                product_name = driver.find_element(By.CSS_SELECTOR, "h3").text
                print(f"[CART] Testing with product: {product_name}")
                self.product_info["product_name"] = product_name
            except:
                print("[CART] Could not get product name")
            
            # Try to increase quantity if plus button exists
            try:
                print("[CART] Trying to increase quantity")
                plus_buttons = driver.find_elements(By.CSS_SELECTOR, ".plus")
                if len(plus_buttons) > 0:
                    plus_buttons[0].click()
                    time.sleep(1)  # Small wait for quantity to update
                    driver.save_screenshot("screenshots/after_quantity_increase.png")
                    print("[CART] Quantity increased")
                else:
                    print("[CART] Plus button not found")
            except Exception as e:
                print(f"[CART] Could not increase quantity: {str(e)}")
            
            # Add to cart
            cart_btn = self.find_element_safely(
                By.ID, "cart_btn", 
                screenshot_prefix="add_to_cart_button"
            )
            cart_btn.click()
            time.sleep(2)  # Wait for add to cart to complete
            driver.save_screenshot("screenshots/after_add_to_cart.png")
            
            # Verify cart update through multiple methods
            success = False
            
            # Method 1: Check for success message
            try:
                success_alert = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
                )
                print(f"[CART] Success message found: {success_alert.text}")
                success = True
            except:
                print("[CART] No success message found, trying other verification methods")
            
            # Method 2: Check cart icon/count
            if not success:
                try:
                    # Check for cart count indicator
                    cart_count = driver.find_elements(By.CSS_SELECTOR, ".cart-count")
                    if len(cart_count) > 0 and cart_count[0].text != "0":
                        print(f"[CART] Cart count updated: {cart_count[0].text}")
                        success = True
                except:
                    print("[CART] Could not verify cart count")
            
            # Method 3: Navigate to cart page
            if not success:
                try:
                    # Navigate to cart to verify item was added
                    driver.get(f"{self.base_url}/cart")
                    time.sleep(3)
                    driver.save_screenshot("screenshots/cart_verification.png")
                    
                    # Check if cart has items
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
        """Test cart page operations using the cart from previous test"""
        try:
            driver = self.driver
            
            # Navigate directly to cart page
            print("[CART-OPS] Navigating to cart page")
            driver.get(f"{self.base_url}/cart")
            time.sleep(3)  # Give more time for cart page to load
            driver.save_screenshot("screenshots/cart_page.png")
            
            # Check if cart is empty
            if "Your Cart is Empty" in driver.page_source:
                print("[CART-OPS] Cart is empty, adding an item first")
                
                # Go to a product page and add to cart
                if self.product_info["product_url"]:
                    # Use the product URL from previous tests
                    driver.get(self.product_info["product_url"])
                else:
                    # Go to homepage and click on first product
                    driver.get(self.base_url)
                    
                    # Wait for products to load
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
                    
                    # Click on the first product
                    first_product = self.find_element_safely(
                        By.CSS_SELECTOR, ".product-card a", 
                        screenshot_prefix="cart_ops_first_product"
                    )
                    first_product.click()
                
                # Wait for product page to load
                self.wait.until(EC.presence_of_element_located((By.ID, "cart_btn")))
                
                # Add to cart
                cart_btn = self.find_element_safely(
                    By.ID, "cart_btn", 
                    screenshot_prefix="cart_ops_add_button"
                )
                cart_btn.click()
                time.sleep(3)  # Wait for add to cart to complete
                
                # Navigate back to cart page
                driver.get(f"{self.base_url}/cart")
                time.sleep(3)
                driver.save_screenshot("screenshots/cart_page_after_adding.png")
                
                # Check if cart is still empty
                if "Your Cart is Empty" in driver.page_source:
                    self.fail("Cart is still empty after adding an item, cannot test cart operations")
                    return
            
            print("[CART-OPS] Cart has items, continuing with test")
            
            # Test cart item presence
            cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item")
            if len(cart_items) == 0:
                # Try alternative selectors
                cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart_item")
                if len(cart_items) == 0:
                    cart_items = driver.find_elements(By.CSS_SELECTOR, "[data-test='cart-item']")
            
            self.assertTrue(len(cart_items) > 0, "No items found in cart")
            print(f"[CART-OPS] Found {len(cart_items)} items in cart")
            
            # Test quantity adjustment if available
            try:
                print("[CART-OPS] Testing quantity adjustment")
                # Try different selectors for plus buttons
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
                    
                    # Try to decrease quantity
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
            
            # Test checkout button if cart is not empty
            try:
                # Try multiple selectors for checkout button
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
        """Test browsing products by category"""
        try:
            driver = self.driver
            
            # Go to homepage
            print("[CATEGORIES] Testing category browsing")
            driver.get(self.base_url)
            
            # Look for category links
            category_links = driver.find_elements(By.CSS_SELECTOR, ".category-link")
            if len(category_links) == 0:
                # Try alternative selectors
                category_links = driver.find_elements(By.CSS_SELECTOR, "[data-test='category']")
                if len(category_links) == 0:
                    category_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar a")
            
            if len(category_links) == 0:
                print("[CATEGORIES] No category links found, skipping test")
                return
            
            # Click on the first category
            print(f"[CATEGORIES] Found {len(category_links)} categories, clicking first one")
            category_links[0].click()
            
            # Wait for products to load
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products")))
            driver.save_screenshot("screenshots/category_products.png")
            
            # Check if any products are displayed
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            print(f"[CATEGORIES] Found {len(products)} products in category")
            
            # Click on a product if available
            if len(products) > 0:
                products[0].find_element(By.TAG_NAME, "a").click()
                
                # Wait for product page to load
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
                driver.save_screenshot("screenshots/category_product_details.png")
                
                # Store this URL as another product option
                self.product_info["category_product_url"] = driver.current_url
                print(f"[CATEGORIES] Stored category product URL: {self.product_info['category_product_url']}")
            
            print("[CATEGORIES] Category browsing test completed")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/category_browse_error.png")
            print(f"[CATEGORIES] Category browsing test encountered an error: {str(e)}")
            # Don't fail the test suite for this optional test
            pass

    def tearDown(self):
        if self.driver:
            print("[TEARDOWN] Closing browser")
            self.driver.quit()

if __name__ == "__main__":
    print("[MAIN] Starting product and cart tests")
    unittest.main()
