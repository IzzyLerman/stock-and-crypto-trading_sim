from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import user

session = Session()



class Setup:
    def __init__(self) -> None:
        pass
    def setup(n):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':f'{n}',
        'convert':'USD',
        'sort':'market_cap'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'a979658d-dbb0-4fed-82ed-177c6365457f',
        }

        with open('userinfo.txt') as f:
            lines = [line.rstrip() for line in f]
        name = lines[0]
        bankroll = float(lines[1])
        curr_user = user.User(name,bankroll)
        curr_user.starting_bankroll = float(lines[2])
        n_coins = int(float(lines[3]))
        x = 4
        for i in range(n_coins):
            curr_user.portfolio.append(user.UserCoin)
            curr_user.portfolio[i].quantity = float(lines[x])
            x+=1
            curr_user.portfolio[i].name = lines[x]
            x+=1
            curr_user.portfolio[i].price = float(lines[x])
            x+=1
            curr_user.portfolio[i].market_cap = float(lines[x])
            x+=1
            curr_user.portfolio[i].symbol = lines[x]
            x+=1
            curr_user.portfolio[i].percent_change_24h = float(lines[x])
            x+=1
            curr_user.portfolio[i].percent_change_7d = float(lines[x])

        
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        coins = []
        coin_name_list = []
        for coin in data["data"]:
            quote = coin["quote"]["USD"]
            coins.append(user.MarketCoin(coin["name"],quote["price"],quote["market_cap"],coin["symbol"],quote["percent_change_24h"],quote["percent_change_7d"]))
            coin_name_list.append(coin["name"])
        
        return coins, coin_name_list, curr_user