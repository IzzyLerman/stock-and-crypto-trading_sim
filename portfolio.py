import PySimpleGUI as sg

class Portfolio:
    def setup_layout(curr_user):

        coin_info_layouts = []
        for i in range(len(curr_user.portfolio)):
            coin_info_layouts.append([[sg.Frame('',[[sg.Text(f'Coin name: {curr_user.portfolio[i].name} ({curr_user.portfolio[i].symbol})',k=f'-COINNAME{i}-')],
                            [sg.Text(f'Price: ${curr_user.portfolio[i].price:,.2f}',k=f'-USERCOINPRICE{i}-')],
                            [ sg.Text(f'Quantity: {curr_user.portfolio[i].quantity} $({curr_user.portfolio[i].quantity*curr_user.portfolio[i].price:,.2f})',k=f'-USERCOINQUANTITY{i}-')],
                            [sg.Text(f'7-day Percent Change: {curr_user.portfolio[i].percent_change_7d:.05f}%',k=f'-PERCENTCHANGE7D{i}-')]],k=f'-COINBOX{i}-')]])
        coin_display = [[sg.Frame('',[[sg.Text(f"USD Balance: ${curr_user.bankroll:.2f}",k='-USERBANKROLLPORTFOLIO-')]])],
                        [sg.Frame('',[[sg.Text("Your Coins:")]])],
                        [sg.Column([],k='-USERCOINS-')]]
        
        coin_display += ([[sg.Frame('',[[sg.Text("Once you buy a coin, it will appear here.")]],visible=len(curr_user.portfolio) == 0,k='-COINBOXTOOLTIP-')]])
        for i in range(len(curr_user.portfolio)):
            coin_display += coin_info_layouts[i]
        coin_display += [[sg.Button("Buy/Sell Crypto",k='-GOTOPURCHASE1-')]]
        portfolio_info = [
                           [sg.Text(f"Your portfolio value: ${curr_user.portfolio_value():,.2f}",k='-PORTFOLIOVALUE-')],
                           [sg.Text(f"Net Change: ${curr_user.net_diff():.2f} ({curr_user.net_diff_percent():.5f}%)",k='-PORTFOLIONETCHANGE-'),sg.VPush()],
                           [sg.Text("Edit your bankroll: ")],
                           [sg.InputText(k='-SETBANKROLL-')],
                           [sg.Button("Edit my Bankroll",k='-EDITBANKROLL-')]]
        


        layout_l = [[sg.Button("Main Menu",k='-GOTOMAINMENU1-')]]+portfolio_info
        
        layout = [[sg.Column(layout_l, element_justification = "center"),sg.Column(coin_display,element_justification = "center",scrollable=False)]]
        return layout
    
    def update_layout(curr_user, window, events, values):
        for i in range(len(curr_user.portfolio)):
            window[f'-USERCOINPRICE{i}-'].update(f'Price: ${curr_user.portfolio[i].price:.2f}')
            window[f'-USERCOINQUANTITY{i}-'].update(f'Quantity: {curr_user.portfolio[i].quantity} $({curr_user.portfolio[i].quantity*curr_user.portfolio[i].price:.2f})')
            window[f'-PERCENTCHANGE7D{i}-'].update(f'7-day Percent Change: {curr_user.portfolio[i].percent_change_7d:.05f}%')
        window['-PORTFOLIOVALUE-'].update(f"Your portfolio value: ${curr_user.portfolio_value():,.2f}")
        window['-PORTFOLIONETCHANGE-'].update(f"Net Change: ${curr_user.net_diff():,.2f} ({curr_user.net_diff_percent():.5f}%)")
        window['-USERBANKROLLPORTFOLIO-'].update(f"USD Balance: ${curr_user.bankroll:,.2f}")

