from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd


def setup_driver():
    """Sets up Chrome options and returns a headless Chrome webdriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver


def get_product_details(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    modal_content = soup.find(id="offerModal___BV_modal_content_")
  
    if not modal_content:
        return None


    product_details = {
        "title": modal_content.find('h2').find('span').text,
        "price": modal_content.find(class_="color-primary-dark").text,
        "images": [img['src'] for img in modal_content.find_all('img')],
    }
    return product_details


def scrape_products(url, max_pages=1):

    driver = setup_driver()
    driver.get(url)

    products = []
    page = 1
    while page <= max_pages:
        try:
            # Find all product cards
            product_cards = driver.find_elements(By.CLASS_NAME, 'item-card-container')

            for card in product_cards:
                # Click the card to open the modal
                card.click()
            
                time.sleep(2)  # Wait for modal to open

                # Extract product details
                product_details = get_product_details(driver)
                if product_details:
                    products.append(product_details)

                # Close the modal
                driver.find_element(By.CLASS_NAME, 'modal-back-button').click()
                time.sleep(3)  # Wait for modal to close

            # Simulate infinite scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Wait for new products to load

            page += 1
        except Exception as e:
            print(f"Error encountered on page {page}: {e}")
            break

    driver.quit()
    return products


if __name__ == "__main__":
    url = 'https://offers-jo.khatawat.store/home/#/'
    scraped_products = scrape_products(url)

    df = pd.DataFrame(scraped_products)
    df.to_excel('product_details.xlsx', index=False)
    # for product in scraped_products:
    #     print(product)
