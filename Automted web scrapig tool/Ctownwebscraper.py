

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl
from datetime import datetime, timedelta

def fetch_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="table_1"]')))
    
    show_all_button = driver.find_element(By.XPATH,'//*[@id="table_1_length"]/label/div/button/span[1]')
    show_all_button.click()

    time.sleep(5)

    return driver.page_source


    

def scrape_and_save_to_excel():
    url = 'https://www.ctmarket.co.za/daily-prices/'
    response = fetch_page(url)

    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find_all('table', class_= 'wpDataTable')




    if table:
      
        # Save the table to an Excel file
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        row_idx =1

        for table_elem in table:
            for row in table_elem.find_all('tr'):
                for col_idx, cell in enumerate(row.find_all('td'), 1):
                    sheet.cell(row=row_idx, column=col_idx, value=cell.get_text())
                    row_idx += 1
        file_name = f"Ctmarket_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        workbook.save(file_name)


