from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

# Open the webpage
driver.get('https://offers-jo.khatawat.store/home/#/')

# Function to parse product details
def get_product_details():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    modal_content = soup.find(id="offerModal___BV_modal_content_")
    if not modal_content:
        return None
    
    product_details = {
        "title": modal_content.find('h2').find('span').text,
        "price": modal_content.find(class_="color-primary-dark").text,
        "images": [img['src'] for img in modal_content.find_all('img')]
    }
    return product_details

# Infinite scroll and product details extraction
products = []
action = ActionChains(driver)

while True:
    try:
        # Get all product cards
        product_cards = driver.find_elements(By.CLASS_NAME, 'item-card-container')
        
        for card in product_cards:
            # Click the product card to open the modal
            card.click()
            time.sleep(2)  # Wait for modal to open

            # Extract product details
            product_details = get_product_details()
            if product_details:
                products.append(product_details)

            # Close the modal
            driver.find_element(By.CLASS_NAME, 'modal-back-button').click()
            time.sleep(1)  # Wait for modal to close

        # Scroll to load more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new products to load

    except Exception as e:
        print(f"Exception encountered: {e}")
        break

driver.quit()

for product in products:
    print(product)
