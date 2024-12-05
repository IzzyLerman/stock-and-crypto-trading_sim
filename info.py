import PySimpleGUI as sg
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decimal import Decimal
from dotenv import load_dotenv
import os


load_dotenv()
summary_port = os.getenv('SUMMARY_PORT')
logo_port = os.getenv('LOGO_PORT')

class Info:
    def __init__(self):
        pass
    def setup_layout(curr_user):
        user_coin_names = [c.name for c in curr_user.portfolio]
        search = [[sg.Combo(user_coin_names,default_value='Select a coin', k='-INFOCHOICE-',readonly=True), sg.Button('View this coin in-depth', k='-VIEWINDEPTH-')]]
        info_panel = [[sg.Image('./logos/64/empty.png',k='-LOGO-'), sg.Text('',k='-INFOTITLE-')]]
        stats = [[sg.Text('',k='-PRICESTAT-',size=(20,4))],
                 [sg.Text('',k='-MARKETCAPSTAT-',size=(20,4))],
                 [sg.Text('',k='-24HSTAT-',size=(20,4))],
                 [sg.Text('',k='-7DSTAT-',size=(20,4))]]
        information = [[sg.Frame('Summary',[[sg.Text('When you select a coin, a summary will appear here.',k='-INFOSUMMARY-',size = (60,20))]]),sg.Frame('Stats',[[stats]])]]
        layout = search + info_panel + information
        return layout
    
    def update_info_page(window, curr_user,coin_name):
        found = False
        for c in curr_user.portfolio:
            if c.name == coin_name:
                curr = c
                found = True
        if(not found):
            return False
        try:
            response = requests.get(f'http://localhost:{summary_port}/summary/{curr.symbol}&{coin_name}')
            summary = response.json()['summary']
            window['-INFOSUMMARY-'].update(summary)
            window['-INFOTITLE-'].update(coin_name)
            window['-PRICESTAT-'].update(f'Price: ${curr.price:,.2f}')
            window['-MARKETCAPSTAT-'].update(f'Market Cap: ${curr.market_cap:,.2f}')
            window['-24HSTAT-'].update(f'24-Hour Change: {curr.percent_change_24h:,.4f}%')
            window['-7DSTAT-'].update(f'7-Day Change: {curr.percent_change_7d:,.4f}%')
        except ConnectionError as e:
            return False
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            return False
        try:
            response = requests.get(f'http://localhost:{logo_port}/logo/{curr.symbol.lower()}')
            path = response.json()['logo']
        except Exception as e:
            print(getattr(e, 'error with logo /'+'message', repr(e)))
            return False
        window['-LOGO-'].update(path)
        return True
        
        