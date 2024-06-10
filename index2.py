import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


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


def get_product_details(soup):
    modal_content = soup.find(id="offerModal___BV_modal_content_")

    if not modal_content:
        return None

    product_details = {
        "title": modal_content.find('h2').find('span').text,
        "price": modal_content.find(class_="color-primary-dark").text,
        "images": [img['src'] for img in modal_content.find_all('img')],
    }
    return product_details


def scrape_product_cards(driver):
    """Scrapes product cards and returns a list of product details."""
    product_details_list = []

    product_cards = driver.find_elements(By.CLASS_NAME, 'item-card-container')

    for card in product_cards:
        # Click the card to open the modal
        card.click()

        time.sleep(2)  # Wait for modal to open

        # Extract product details
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_details = get_product_details(soup)
        if product_details:
            product_details_list.append(product_details)

        # Close the modal
        driver.find_element(By.CLASS_NAME, 'modal-back-button').click()
        time.sleep(3)  # Wait for modal to close

    return product_details_list


def scroll_down(driver):
    """Scrolls down to load more products."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new products to load


def scrape_products(url, max_pages=1):
    """Scrapes products from the given URL."""
    driver = setup_driver()
    driver.get(url)

    products = []
    page = 1
    prev_num_products = 0  # Track number of products to detect when no more products are loaded
    while page <= max_pages:
        try:
            product_details_list = scrape_product_cards(driver)
            products.extend(product_details_list)

            # Scroll down to load more products
            scroll_down(driver)

            # Count number of products after scrolling
            current_num_products = len(driver.find_elements(By.CLASS_NAME, 'item-card-container'))

            # Check if new products are loaded
            if current_num_products == prev_num_products:
                break  # No more new products loaded, exit loop

            prev_num_products = current_num_products  # Update the number of products

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
