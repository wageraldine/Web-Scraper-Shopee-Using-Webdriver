# shopee.py
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path=r'chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)
katakunci = input('Masukkan kata kunci : ')
def search(katakunci):
    links = []
    print('mencari semua product dengan kata kunci ' + katakunci)
    url = 'https://shopee.co.id/search?keyword=' + katakunci
    try:
        driver.get(url)
        time.sleep(10)
        driver.execute_script('window.scrollTo(0, 2000);')
        time.sleep(10)
        driver.execute_script('window.scrollTo(0, 3000);')
        time.sleep(10)
        soup_a = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup_a.find('ul', class_='row shopee-search-item-result__items')
        for link in products.find_all('a'):
            links.append(link.get('href'))
            print(link.get('href'))
    except TimeoutException:
        print('failed to get links with query ')
    return links

def get_product(produt_url):
    try:
        url = 'https://shopee.co.id' + produt_url
        print(url)
        driver.get(url)
        time.sleep(10)
        driver.execute_script('window.scrollTo(0, 5000);')
        time.sleep(10)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'rqONlU')))
        soup_b = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup_b.find('h1', class_='rqONlU').text
        price = soup_b.find('div', class_='Y3DvsN').text
        try:
            imgurl = soup_b.find('img', class_='_7D4JtJ')['src']
        except:
            imgurl = 'none'
        desc = soup_b.find('p', class_='irIKAp').text
        print('Scraping ' + title)
        with open('result.csv','a', encoding='utf-8',newline='') as f:
            writer=csv.writer(f)
            writer.writerow([title,price,url,desc,imgurl])

    except TimeoutException:
        print('cant open the link')

products_urls = search(katakunci)

for product_url in products_urls:
    get_product(product_url)

driver.quit()