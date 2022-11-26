import requests
from bs4 import BeautifulSoup


class Get_Coins:
    def __init__(self):
        pass

    def get_all_coins(self, url='https://coinmarketcap.com'):
        _headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'
        }

        #get content
        response = requests.get(url, headers=_headers).text
        soup = BeautifulSoup(response, 'lxml')

        coins = soup.find('tbody').find_all('tr')
        all_coins = {}

        for coin in coins:
            coin_name = coin.find(class_='cmc-link').get('href').replace('/currencies/', '')[:-1]
            coin_price = coin.find(class_='sc-131di3y-0 cLgOOr')
            if coin_name:
                try:
                    all_coins[coin_name] = coin_price.text
                except:
                    coin_price = coin.find_all('td')[-2].text
                    all_coins[coin_name] = coin_price

        return all_coins