from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from utils import check_popup


def summary(driver):
    print(f"Summary {driver.current_url}")
    table = driver.find_element(By.XPATH, '//*[@id="quote-summary"]')
    table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
    dividend_row = table_soup.find(
        'span', text="Forward Dividend & Yield").parent.parent
    dividend_yield = dividend_row.find_all('td')[1].text
    print(f' - dividend yield: {dividend_yield}')
    pe_row = table_soup.find('span', text="PE Ratio (TTM)").parent.parent
    pe_ratio = pe_row.find_all('td')[1].text
    print(f' - PE ratio: {pe_ratio}')
    prev_close_row = table_soup.find(
        'span', text="Previous Close").parent.parent
    prev_close = prev_close_row.find_all('td')[1].text
    print(f' - prev close: {prev_close}')
    print("")


def financials(driver, stock):
    driver.get(
        f'https://finance.yahoo.com/quote/{stock}/financials?p={stock}')
    check_popup(driver)
    print(f"Income statement ({driver.current_url})")
    table = driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div')
    table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
    total_revenue_row = table_soup.find(
        'span', text="Total Revenue").parent.parent.parent
    total_revenue = total_revenue_row.find_all('span')[1].text
    operating_income_row = table_soup.find(
        'span', text="Operating Income").parent.parent.parent
    operating_income = operating_income_row.find_all('span')[1].text
    print(f' - total revenue: {total_revenue}')
    print(f' - operating income: {operating_income}')
    print(
        ' - ratio of operating income to total revenue (>15%): {:.2f}%'.format(
            float(operating_income.replace(",", ""))/float(total_revenue.replace(",", ""))*100))
    print("")


def balance_sheet(driver, stock):
    driver.get(
        f'https://finance.yahoo.com/quote/{stock}/balance-sheet?p={stock}')
    check_popup(driver)
    print(f"Balance sheet ({driver.current_url})")
    driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/button').click()
    driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/button').click()

    table = driver.find_element(
        By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div')
    table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

    current_assets_row = table_soup.find(
        'span', text="Current Assets").parent.parent.parent
    current_assets = current_assets_row.find_all('span')[1].text
    print(f' - current assets: {current_assets}')

    current_liabilities_row = table_soup.find(
        'span', text="Current Liabilities").parent.parent.parent
    current_liabilities = current_liabilities_row.find_all('span')[1].text
    print(f' - current liabilities: {current_liabilities}')
    print(
        ' - Ratio current assets / current liabilities (>1 good): {:.2f}'.format(
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
