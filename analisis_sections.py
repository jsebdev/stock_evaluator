from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from utils import check_popup
from lxml import etree


def summary(driver):
    print("Summary")
    print(driver.current_url)
    dividend_yield = driver.find_element(
        By.XPATH, '//*[@id="quote-summary"]/div[2]/table/tbody/tr[6]/td[2]')
    print(f' - dividend yield: {dividend_yield.text}')
    pe_ratio = driver.find_element(
        By.XPATH, '//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]')
    print(f' - PE ratio: {pe_ratio.text}')
    prev_close = driver.find_element(
        By.XPATH, '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]')
    print(f' - prev close: {prev_close.text}')
    print("")


def financials(driver, stock):
    driver.get(
        f'https://finance.yahoo.com/quote/{stock}/financials?p={stock}')
    check_popup(driver)
    print("Income statement")
    print(driver.current_url)
    total_revenue = driver.find_element(
        By.XPATH, '// *[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[2]/span').text
    print(f' - total revenue: {total_revenue}')
    operating_income = driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[5]/div[1]/div[2]/span').text
    print(f' - operating income: {operating_income}')
    print(
        'ratio of operating income to total revenue (>15%): {:.2f}%'.format(
            float(operating_income.replace(",", ""))/float(total_revenue.replace(",", ""))*100))
    print("")


def balance_sheet(driver, stock):
    driver.get(
        f'https://finance.yahoo.com/quote/{stock}/balance-sheet?p={stock}')
    # print(f'74: get_url >>>\n{driver.current_url}')
    # click to show current assets and current liabilities
    check_popup(driver)
    print("Balance sheet")
    print(driver.current_url)
    driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/button').click()
    current_assets = driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span').text
    print(f' - current assets: {current_assets}')
    driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/button').click()
    current_liabilities = driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/span').text
    print(f' - current liabilities: {current_liabilities}')
    print(
        'ratio current assets / current liabilities (>1 good): {:.2f}'.format(
            float(current_assets.replace(",", "")) /
            float(current_liabilities.replace(",", ""))
        ))
    print("")


def cash_flow(driver, stock):
    driver.get(
        f'https://finance.yahoo.com/quote/{stock}/cash-flow?p={stock}')
    print(f'Cash flow (last 5 years) ({driver.current_url})')
    table = driver.find_element(
        By.XPATH,    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div')
    table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
    # print(f'95: table_soup >>>\n{table_soup}')
    cash_flow_row = table_soup.find(
        'span', text="Free Cash Flow").parent.parent.parent
    # print(f'97: cash_flow_row >>>\n{cash_flow_row}')
    cash_flows = cash_flow_row.find_all('span')
    cash_flows = list(map(lambda x: x.text, cash_flows))
    # print(f'102: cash_flows >>>\n{cash_flows}')

    heade_row = table_soup.find('div', class_='D(tbr)')
    headers = heade_row.find_all('span')
    headers = list(map(lambda x: x.text, headers))
    # print(f'105: headers >>>\n{headers}')
    # print(f'101: cash_flows >>>\n{cash_flows}')
    for t, cf in zip(headers[1:], cash_flows[1:]):
        print(' - {:<20}${}'.format(t, cf))
