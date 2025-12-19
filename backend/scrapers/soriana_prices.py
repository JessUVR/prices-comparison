from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_soriana_prices():
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless=new")  # Run browser in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize WebDriver (Selenium Manager will handle ChromeDriver automatically)
    driver = webdriver.Chrome(options=options)

    try:
        # URL to scrape
        url = "https://www.soriana.com/cervezas"
        driver.get(url)

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        products = []

        # Loop through product elements
        for item in soup.select(".product-tile"):
            name = item.select_one(".product-title")
            name = name.text.strip() if name else "No name found"

            price = item.select_one(".product-sales-price")
            price = price.text.strip() if price else "No price found"

            img = item.select_one("img")
            img_url = img["src"] if img and "src" in img.attrs else "No image found"

            products.append({
                "name": name,
                "price": price,
                "image": img_url
            })

        return products

    finally:
        # Close the browser
        driver.quit()

        