from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

CHROME_DRIVER_PATH = "chromedriver"

def run():
    # Configure browser options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

    try:
        print("🚀 Opening Soriana website...")
        driver.get("https://www.soriana.com")
        time.sleep(3)

        print("📍 Attempting to close location modal...")
        driver.execute_script('''
            const btn = document.querySelector('[data-testid="btn-continue"]');
            if (btn) { btn.click(); return true; } else { return false; }
        ''')
        time.sleep(2)

        print("🔍 Searching for milk...")
        search_input = driver.find_element(By.NAME, "search")
        search_input.send_keys("leche")
        search_input.submit()
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = []

        containers = soup.find_all("div", class_="tile-body product-tile__body w-100 p-0")
        for item in containers:
            try:
                name = item.find("a", class_="link plp-Link font-primary--regular product-tile--link ellipsis-product-name font-size-16").text.strip()
            except:
                name = "No name"

            try:
                price = item.find("span", class_="cart-price price-plp price-not-found price-pdp pr-0 font-size-14 font-size-14 cart-price-option-b").text.strip()
            except:
                price = "No price"

            products.append({
                "name": name,
                "current_price": price,
                "store": "Soriana"
            })

        return products

    finally:
        driver.quit()
