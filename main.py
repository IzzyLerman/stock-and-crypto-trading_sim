import PySimpleGUI as sg
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from decimal import Decimal


import user
import setup
import purchase
import portfolio

n= 10
userinfo = "userinfo.txt"
#curr_user = curr_user.User("izzy",10000)
sg.theme('Dark Green 4')
# All the stuff inside your window.
coins, coin_name_list, curr_user = setup.Setup.setup(n)

purchase_layout = purchase.Purchase.setup_layout(coins, curr_user, n)
# Create the Window
portfolio_layout = portfolio.Portfolio.setup_layout(curr_user)


layout = [[sg.Column(portfolio_layout, element_justification="center",visible=True,k="-PORTFOLIOPAGE-"),sg.Column(purchase_layout,element_justification="center",visible=False,k='-PURCHASEPAGE-')]]

window = sg.Window('Window Title', layout)


curr_screen = "purchase"
coin_is_selected = False
mode = "Buy"


# Event Loop to process "events" and get the "values" of the inputs
while True:
    try:
        pass
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel': # if curr_user closes window or clicks cancel
            break   
    if event == '-GOTOPURCHASE-':
        window['-PORTFOLIOPAGE-'].update(visible = False)
        window['-PURCHASEPAGE-'].update(visible=True)
        window['-USERBANKROLL-'].update(f"Your Bankroll :${curr_user.bankroll}")
    if event == '-GOTOPORTFOLIO-':
        window['-PORTFOLIOPAGE-'].update(visible = True)
        window['-PURCHASEPAGE-'].update(visible=False)
        portfolio.Portfolio.update_layout(curr_user,window,event,values)
    if event == '-EDITBANKROLL-':
        if values['-SETBANKROLL-'] == '':
            sg.popup("Error: choose a value for your bankroll!", title = "Error")
        else:
            curr_user.bankroll = float(values['-SETBANKROLL-'])
            curr_user.starting_bankroll = float(values['-SETBANKROLL-'])
            portfolio.Portfolio.update_layout(curr_user,window,event,values)
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
    

    
curr_user.write(userinfo)
window.close()
