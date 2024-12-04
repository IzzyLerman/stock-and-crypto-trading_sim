import PySimpleGUI as sg
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decimal import Decimal
from dotenv import load_dotenv
import os


import user
from setup import Setup
from purchase import Purchase
from portfolio import Portfolio
from mainMenu import MainMenu 


load_dotenv()
notif_port = os.getenv('NOTIF_PORT')
n= 100
userinfo = "./userinfo.txt"
sg.theme('Dark Green 4')
purchase_page = Purchase()
coins, coin_name_list, curr_user = Setup.setup(n)

purchase_layout = purchase_page.setup_layout(coins, curr_user,3)
portfolio_layout = Portfolio.setup_layout(curr_user)
main_menu_layout = MainMenu.setup_layout()

PAGE_KEYS = ["-PORTFOLIOPAGE-",'-PURCHASEPAGE-','-MAINMENUPAGE-']

layout = [[sg.Column(portfolio_layout, element_justification="center",visible=False,k="-PORTFOLIOPAGE-"),
           sg.Column(purchase_layout,element_justification="center",visible=False,k='-PURCHASEPAGE-'),
           sg.Column(main_menu_layout,element_justification="center",visible=True,k='-MAINMENUPAGE-')]]

window = sg.Window('Window Title', layout)

curr_screen = "purchase"
coin_is_selected = False
mode = "Buy"

def switch_to_page(key, window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width,win_height = window.size
    x, y = (screen_width - win_width) // 2, win_height//10
    window.move(x,y)
    for k in PAGE_KEYS:
        if k != key:
            window[k].update(visible=False)
        else:
            window[k].update(visible=True)

## Returns a tuple with the JSON response and a flag indicating success or not

def send_coin_to_notif(coin):
    notification_data = {
        "asset_symbol": coin.symbol,
        "alert_value": coin.price,  # Use a number here instead of a string
        "notification_type": "Price Alert",
        "user_email": curr_user.email  # Add user email to the request
    }

    try:
        response = requests.post(f"http://localhost:{notif_port}/notify", json=notification_data)
        if response.status_code == 200:
            return response.json(), True
        else:
            return response.json(), False
    except ConnectionError as e:
        return {}, False
    except Exception as e:
        print(getattr(e, 'message', repr(e)))
        return {}, False

def generate_notif(res, window):
    price = res['alert']['alert_value']
    window['-NOTIFRESPONSE-'].update(visible=True)
    window['-NOTIFYSYMBOL-'].update(res['alert']["asset_symbol"]+'\t$'+f'{price:,.2f}')
    window['-NOTIFTYPE-'].update('Notification Type: '+res['alert']["notification_type"])
    window['-NOTIFMSG-'].update(res["message"])
    pass

while True:
    try:
        pass
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel': # if curr_user closes window or clicks cancel
            break   
    
    ## Page switches

    if event in [f'-GOTOPURCHASE{i}-' for i in range(5)]:
        switch_to_page('-PURCHASEPAGE-', window)
        window['-USERBANKROLL-'].update(f"Your Bankroll :${curr_user.bankroll}")
    if event in [f'-GOTOPORTFOLIO{i}-' for i in range(5)]:
        switch_to_page('-PORTFOLIOPAGE-', window)
        Portfolio.update_layout(curr_user,window,event,values)
    if event in [f'-GOTOMAINMENU{i}-' for i in range(5)]:
        switch_to_page('-MAINMENUPAGE-',window)

    ## Portfolio Page

    if event == '-EDITBANKROLL-':
        if values['-SETBANKROLL-'] == '':
            sg.popup("Error: choose a value for your bankroll!", title = "Error")
        else:
            result = sg.popup(f"You are about to set your bankroll to ${values['-SETBANKROLL-']} - Are you sure?",custom_text=("I'm sure","Nevermind"))
            if result == "I'm sure":
                curr_user.bankroll = float(values['-SETBANKROLL-'])
                curr_user.starting_bankroll = float(values['-SETBANKROLL-'])
                Portfolio.update_layout(curr_user,window,event,values)
    if event == '-NOTIFY-':
        symb = values['-NOTIFYLIST-']
        if symb == 'Select a coin':
            sg.popup("You must select a coin first!",title = "Error")
        else:
            for c in curr_user.portfolio:
                if c.symbol == symb:
                    notif_response, status = send_coin_to_notif(c)
            if status:
                generate_notif(notif_response, window)
            else:
                sg.Popup("Failed to connect to the notification service. Is it running?", title="Couldn't connect")

    ## Purchase Page

    for i in range(n):
        if event == f'-BUYCOIN{i}-':
            selected = coins[i]
            selected_owned = 0
            for c in curr_user.portfolio:
                if c.name == selected.name:
                    selected_owned = c.quantity
            coin_is_selected = True
            window['-SELECTEDCOIN-'].update(f"Selected Coin: {selected.name} ({selected.symbol})")
            window['-SELECTEDPRICE-'].update(f'Price: ${selected.price:0.2f}',visible=True)
            window['-SELECTEDQUANTITYOWNED-'].update(f"You own: {selected_owned:.5f} {selected.symbol} (${selected_owned*selected.price:.2f})",visible=True)
            window['-HOWMUCH-'].update(visible=True)
    if event == '-BUYORSELL-':
        mode = values['-BUYORSELL-']
        window['-PURCHASE-'].update(f'{mode}')

    if event == '-PURCHASE-':
        if not coin_is_selected:
            sg.popup('Error: No coin selected! Choose a coin first.',title='No Coin Selected!')
        elif values['-QUANTITYINPUT-'] == '':
            sg.popup('Error: Must specify how much you want to buy.', title='Missing Quantity')
        else:
            quantity = float(values['-QUANTITYINPUT-'])
            success, last_of_inv = curr_user.purchase(selected,quantity,mode)
            if success == -2:
                sg.popup(f"You don't have enough money to buy {quantity} of {selected.name}.")
            elif success == -3:
                sg.popup(f"You don't have {quantity} of {selected.name}!")

            else: 
                if last_of_inv:
                    window[f'-COINBOX{success}-'].update(visible=False)
                elif success !=-1:
                    i = success
                    #if purchase returns -2, we must make a new box for that type of coin on the portfolio page
                    user_coin_box = [[sg.Frame('',[[sg.Text(f'Coin name: {curr_user.portfolio[i].name} ({curr_user.portfolio[i].symbol})',k=f'-COINNAME{i}-')],
                                [sg.Text(f'Price: ${curr_user.portfolio[i].price:.2f}',k=f'-USERCOINPRICE{i}-')],
                                [ sg.Text(f'Quantity: {curr_user.portfolio[i].quantity} $({curr_user.portfolio[i].quantity*curr_user.portfolio[i].price:.2f})',k=f'-USERCOINQUANTITY{i}-')],
                                [sg.Text(f'7-day % change: {curr_user.portfolio[i].percent_change_7d:.05f}%',k=f'-PERCENTCHANGE7D{i}-')]],k=f'-COINBOX{i}-')]]
                    window['-COINBOXTOOLTIP-'].update(visible=False)
                    window.extend_layout(window['-USERCOINS-'], user_coin_box)
                selected_usercoin = curr_user.get_coin(selected)
                selected_owned = selected_usercoin.quantity if selected_usercoin is not None else 0
                window['-SELECTEDQUANTITYOWNED-'].update(f"You own: {selected_owned:.5f} {selected.symbol} (${selected_owned*selected.price:.2f})",visible=True)
                window['-USERBANKROLL-'].update(f"Your Bankroll :${curr_user.bankroll}")
                sg.popup(f"Successfully {'bought' if mode == 'Buy' else 'sold'} {quantity} of {selected.name}!")
    if event == '-SHOWMORECOINS-':
        purchase_page.add_coins_to_purchase(curr_user, window, coins, 3)
    
    

    
curr_user.write(userinfo)
window.close()
