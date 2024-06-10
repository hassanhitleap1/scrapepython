import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')  # Start browser maximized
    options.add_argument('disable-infobars')  # Disable infobars
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_product_details(driver, product_element):
    product_element.click()
    time.sleep(2)  # Wait for modal to load

    # Extract product details
    product_details = {}

    product_details['title'] = driver.find_element(By.ID, 'offerModal___BV_modal_content_').find_element(By.TAG_NAME, 'h2').find_element(By.TAG_NAME, 'span').text
    product_details['price'] =  driver.find_element(By.ID, 'offerModal___BV_modal_content_').find_element(By.CLASS_NAME, 'color-primary-dark').text
    print(  product_details['title'])
    print(  product_details['price'])
    images =  driver.find_element(By.ID, 'offerModal___BV_modal_content_').find_elements(By.CSS_SELECTOR, 'img')
    product_details['images'] = [image.get_attribute('src') for image in images]

    # Close modal
    driver.find_element(By.CSS_SELECTOR, 'button.close').click()
    time.sleep(1)  # Wait for modal to close

    return product_details

def main():
    driver = setup_driver()
    url = 'https://offers-jo.khatawat.store/home/#/'
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Adjust this delay as necessary

    all_product_details = []

    # Get initial product elements
    product_elements = driver.find_elements(By.CLASS_NAME, 'card-container')
    
    # Scroll down to load more products
    for _ in range(5):  # Adjust the number of scrolls as necessary
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # Wait for the page to load more products

    # Get all product elements after scrolling
    product_elements = driver.find_elements(By.CLASS_NAME, 'card-container')

    # Scrape details of all products
    for product_element in product_elements:
        try:
            details = scrape_product_details(driver, product_element)
            all_product_details.append(details)
        except Exception as e:
            print(f"Error scraping product: {e}")

    driver.quit()

    # Export to Excel
    df = pd.DataFrame(all_product_details)
    df.to_excel('product_details.xlsx', index=False)


if __name__ == "__main__":
    main()
