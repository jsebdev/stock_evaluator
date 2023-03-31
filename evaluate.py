import argparse
from bs4 import BeautifulSoup
from analisis_sections import balance_sheet, cash_flow, financials, summary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re


parser = argparse.ArgumentParser(description='get info from a stock')
parser.add_argument('--stocks', nargs='+',
                    help='name of the stock', required=True)
parser.add_argument('--headless', action='store_false')
parser.add_argument('--detach', action='store_true')

args = parser.parse_args()

options = Options()
if args.detach:
    options.add_experimental_option("detach", True)
if args.headless:
    options.add_argument('--headless')

# driver = webdriver.Chrome("/Users/sebastian/Documents/selenium_drivers/chromedriver_mac_arm64")
# for some I don't need to point to the driver I downloaded
driver = webdriver.Chrome(options=options)

stocks = map(str.upper, args.stocks)


for stock in stocks:
    # base_url = 'https://finance.yahoo.com/quote/' + stock
    base_url = f'https://finance.yahoo.com/quote/{stock}/cash-flow?p={stock}'
    # print(f'14: base_url >>>\n{base_url}')
    driver.get(base_url)
    # print(f'30: driver.title >>>\n{driver.title}')

    # content = driver.page_source
    # soup = BeautifulSoup(content)
    # dom = etree.HTML(str(soup))
    if re.search("Requested symbol wasn't found", driver.title):
        print(driver.title)
        continue

    if re.search('lookup', driver.current_url):
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

    if re.search(stock, driver.title, re.IGNORECASE):
        print(f'stock found, {driver.title}', end='\n\n')

        # Summary
        # summary(driver)

        # Income statement
        # financials(driver, stock)

        # Balance sheet
        # balance_sheet(driver, stock)

        # Cash flow
        cash_flow(driver, stock)


driver.quit()
