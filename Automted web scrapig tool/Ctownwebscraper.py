import asyncio
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

async def fetch_table(url):
    try:
        print("Setting up the browser options...")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        
        print(f"Fetching the URL: {url}")
        driver.get(url)
        
        try:
            iframe = driver.find_element(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(iframe)
            print("Switched to iframe")
        except Exception as e:
            print(f"No iframe found: {e}")


        print("Waiting for the button to be present...")
        button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#right2 > div.myform1.myform113 > form > input[type=submit]'))
        )
        print("Clicking the button...")
        button.click()

        print("Waiting for the table to be present...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="right2"]/table'))
        )

        # Wait for the page to reload with all entries displayed
        await asyncio.sleep(5)  

        print("Parsing the page source with BeautifulSoup...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', class_='alltable')

        # Close the driver to avoid resource leaks
        print("Closing the browser...")
        driver.quit()

        if table is None:
            print("No table found on the webpage.")
        else:
            print("Table found and parsed successfully.")

        return table

    except Exception as e:
        print(f"An error occurred in fetch_table: {e}")
        driver.quit()

async def scrape_and_save_to_csv():
    try:
        url = 'https://www.joburgmarket.co.za/jhbmarket/daily-price-list/'
        table = await fetch_table(url)

        if table is None:
            print("No table found, exiting the script.")
            return

        # Extract headers
        print("Extracting headers...")
        headers = [header.text for header in table.find_all('th')]
        
        # Extract rows
        print("Extracting rows...")
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            rows.append([cell.text for cell in row.find_all('td')])

        # Create DataFrame
        print("Creating DataFrame...")
        df = pd.DataFrame(rows, columns=headers)

        # Save to CSV
        filename = f'joburg_market_prices_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        print(f"Saving data to {filename}...")
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    except Exception as e:
        print(f"An error occurred in scrape_and_save_to_csv: {e}")

def main():
    asyncio.run(scrape_and_save_to_csv())

if __name__ == "__main__":
    main()
