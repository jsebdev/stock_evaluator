import argparse
from bs4 import BeautifulSoup
import requests

parser = argparse.ArgumentParser(description='get info from a stock')
parser.add_argument('--stocks', nargs='+',
                    help='name of the stock', required=True)

args = parser.parse_args()

for stock in args.stocks:
    print('searching for ' + stock)
    base_url = 'https://finance.yahoo.com/quote/' + stock
    # base_url = 'https://google.com'
    print(f'14: base_url >>>\n{base_url}')
    r = requests.get(base_url)
    print(r.status_code)
