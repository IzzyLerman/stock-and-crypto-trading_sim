from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os
import user

session = Session()

userinfofilename = './userinfo.txt'


class Setup:
    def __init__(self) -> None:
        pass
    def setup(n):
        load_dotenv()
        API_KEY = os.getenv('API_KEY')
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':f'{n}',
        'convert':'USD',
        'sort':'market_cap'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
        }

        with open(userinfofilename) as f:
            lines = [line.rstrip() for line in f]
        name = lines[0]
        bankroll = float(lines[1])
        curr_user = user.User(name,bankroll)
        curr_user.starting_bankroll = float(lines[2])
        n_coins = int(lines[3])
        if(n_coins == 0):
            pass
        else:
            for i in range(n_coins):
                idx = i*7
                curr_user.portfolio.append(user.UserCoin(
                    float(lines[idx+4]), 
                    lines[idx+5], 
                    float(lines[idx+6]),
                    float(lines[idx+7]),
                    lines[idx+8],
                    float(lines[idx+9]),
                    float(lines[idx+10])
                ))
        
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