import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from lxml import etree


parser = argparse.ArgumentParser(description='get info from a stock')
parser.add_argument('--stocks', nargs='+',
                    help='name of the stock', required=True)

args = parser.parse_args()

options = Options()
# options.headless = True
options.add_argument('--headless')

# driver = webdriver.Chrome("/Users/sebastian/Documents/selenium_drivers/chromedriver_mac_arm64")
# for some I don't need to point to the driver I downloaded
driver = webdriver.Chrome(options=options)


for stock in args.stocks:
    print('searching for ' + stock)
    base_url = 'https://finance.yahoo.com/quote/' + stock
    print(f'14: base_url >>>\n{base_url}')
    driver.get(base_url)
    assert 'Yahoo' in driver.title
    get_url = driver.current_url
    print(f'32: get_url >>>\n{get_url}')

    # content = driver.page_source
    # soup = BeautifulSoup(content)
    # dom = etree.HTML(str(soup))

    if re.search('lookup', get_url):
        print('**** SYMBOL NOT FOUND ****')
        page_title = driver.find_element(
            By.XPATH, '//*[@id="lookup-page"]/section/div/h2/span').get_attribute("innerHTML")
        print(page_title)  # Symbols similar to: 'stock'
        symbols = driver.find_elements(
            By.XPATH, '//*[@id="lookup-page"]/section/div/div/div/div[1]/table/tbody/tr/td[1]/a')
        # print(f'45: len(symbols) >>>\n{len(symbols)}')
        symbols_names = driver.find_elements(
            By.XPATH, '//*[@id="lookup-page"]/section/div/div/div/div[1]/table/tbody/tr/td[2]')
        # print(f'48: len(symbols_names) >>>\n{len(symbols_names)}')
        for symbol, name in zip(symbols, symbols_names):
            print(f' - symbol: {symbol.text} name: {name.text}')
        # symbols = dom.xpath(
        #     '//*[@id="lookup-page"]/section/div/div/div/div[1]/table/tbody/tr[1]/td[1]/a')
        # print(f'52: symbols >>>\n{symbols}')
        continue

    print('stock found')


driver.quit()
