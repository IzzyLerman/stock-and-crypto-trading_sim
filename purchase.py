import PySimpleGUI as sg

class Purchase:
    def setup_layout(coins, user,n):
        coin_info_layouts = []
        coin_box_layouts = []
        for i in range(n):
            coin_info_layouts.append([[sg.Text(f'Coin name: {coins[i].name} ({coins[i].symbol})',k=f'-COINNAME{i}-')],
                            [sg.Text('Price: ${0:.2f}'.format(coins[i].price),k=f'-COINPRICE{i}-')],
                            [ sg.Text('Market Cap: ${0:.2E}'.format(coins[i].market_cap),k=f'-COINMARKETCAP{i}-')]])
            coin_box_layouts.append([sg.Frame('',[[sg.Button(f'Select',k = f'-BUYCOIN{i}-'),sg.Frame('',coin_info_layouts[i],element_justification='center')]])])



        purchase_box = [  
                    [sg.Text("Purchase/Sell Coins Here!") ],
                    [sg.Text("Selected Coin: None",k="-SELECTEDCOIN-")],
                    [sg.Text("Price: ",k='-SELECTEDPRICE-',visible=False)],
                    [sg.Text(f"Your Bankroll :${user.bankroll}",k='-USERBANKROLL-')],
                    [sg.Text(f"You own: ",k='-SELECTEDQUANTITYOWNED-',visible=False)],
                    [sg.Text('How much would you like to exchange?',k='-HOWMUCH-',visible=False)],
                    [sg.Combo(['Buy','Sell'], default_value='Buy',k='-BUYORSELL-',enable_events=True,readonly=True)],
                    [sg.InputText(k='-QUANTITYINPUT-',default_text=1)],
                    [sg.Button('Buy',k='-PURCHASE-')],
                    [sg.VPush()  ]]

        layout_r = []
        for i in range(n):
            layout_r += [coin_box_layouts[i]]
        layout_r += [[sg.VPush()]]

        layout_l = [[sg.Frame('Purchase',purchase_box)],[sg.Button("View my Portfolio in Detail",k='-GOTOPORTFOLIO-')]]

        layout = [[sg.Column(layout_l, element_justification="center"),sg.Column(layout_r, element_justification='right',scrollable=True)]]

        return layout
    

    
        