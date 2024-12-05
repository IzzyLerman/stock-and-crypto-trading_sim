import PySimpleGUI as sg

class Purchase:
    def __init__(self):
        self.num_coins_displayed = 0
        self.coin_boxes = []
        self.market_size = 0
    def setup_layout(self, coins, user,n):
        self.num_coins_displayed = n
        coin_info_layouts = []
        coin_box_layouts = []
        self.market_size = n
        for i in range(n):
            coin_info_layouts.append([[sg.Text(f'Coin name: {coins[i].name} ({coins[i].symbol})',k=f'-COINNAME{i}-')],
                            [sg.Text('Price: ${0:.2f}'.format(coins[i].price),k=f'-COINPRICE{i}-')],
                            [ sg.Text('Market Cap: ${0:.2E}'.format(coins[i].market_cap),k=f'-COINMARKETCAP{i}-')]])
            coin_box_layouts.append([sg.Frame('',[[sg.Button(f'Select',k = f'-BUYCOIN{i}-'),sg.Frame('',coin_info_layouts[i],element_justification='center')]])])



        purchase_box = [  
                    [sg.Text("Purchase/Sell Coins Here!") ],
                    [sg.Text("Selected Coin: None",k="-SELECTEDCOIN-")],
                    [sg.Text("Price: ",k='-SELECTEDPRICE-',visible=False)],
                    [sg.Text(f"Your Bankroll :${user.bankroll:,.2}",k='-USERBANKROLL-')],
                    [sg.Text(f"You own: ",k='-SELECTEDQUANTITYOWNED-',visible=False)],
                    [sg.Text('How much would you like to exchange?',k='-HOWMUCH-',visible=False)],
                    [sg.Combo(['Buy','Sell'], default_value='Buy',k='-BUYORSELL-',enable_events=True,readonly=True)],
                    [sg.InputText(k='-QUANTITYINPUT-',default_text=1)],
                    [sg.Button('Buy',k='-PURCHASE-')],
                    [sg.VPush()  ]]

        coins_to_purchase = []
        for i in range(n):
            coins_to_purchase += [coin_box_layouts[i]]
        self.coin_boxes = coins

        show_more = [[sg.Button(f'Show More Coins',k='-SHOWMORECOINS-')]]

        lookup_input = [[sg.Input(k='-LOOKUPINPUT-',size=(30,5)),sg.Button('Look up coin',k='-LOOKUP-')]]
        lookup = [[sg.Frame('Look up a coin by name', lookup_input)]]

        layout_r = lookup + [[sg.Column(coins_to_purchase,k='-COINSTOPURCHASE-',scrollable=True)]] + show_more

        layout_l = [[sg.Frame('Purchase',purchase_box)],[sg.Button("View my Portfolio in Detail",k='-GOTOPORTFOLIO1-'), sg.Button("Main Menu",k='-GOTOMAINMENU2-')]]

        layout = [[sg.Column(layout_l, element_justification="center"),sg.Column(layout_r, element_justification='right')]]

        return layout
    
    def add_coin_to_market(self, curr_user, window, coins, new_coin):
        coins.insert(self.num_coins_displayed,new_coin)
        self.market_size += 1
        self.add_coins_to_purchase(curr_user,window,coins,1)
    
    def add_coins_to_purchase(self, user, window, coins, n):
        for j in range(n):
            i = j + self.num_coins_displayed
            #print(f'{coins[i].symbol} ')
            coin_info = [[sg.Text(f'Coin name: {coins[i].name} ({coins[i].symbol})',k=f'-COINNAME{i}-')],
                        [sg.Text('Price: ${0:.2f}'.format(coins[i].price),k=f'-COINPRICE{i}-')],
                        [ sg.Text('Market Cap: ${0:.2E}'.format(coins[i].market_cap),k=f'-COINMARKETCAP{i}-')]]
            coin_box = [[sg.Frame('',[[sg.Button(f'Select',k = f'-BUYCOIN{i}-'),sg.Frame('',coin_info,element_justification='center')]])]]
            window.extend_layout(window['-COINSTOPURCHASE-'],coin_box)
        self.num_coins_displayed += n
        window.refresh()
        window['-COINSTOPURCHASE-'].contents_changed()
            

    

    
        