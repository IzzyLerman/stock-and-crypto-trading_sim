import PySimpleGUI as sg

class MainMenu:
    def setup_layout():
        welcome_panel = [[sg.Frame('',[[sg.Text("Welcome to CryptoGenius!")],
            [sg.Text("Test out your trading skills against real-time data!")],
            [sg.Text("Make some trades, then come back tomorrow to see how you would have done in the real market!")],
            [sg.Text("Trading only takes a couple clicks!")]])],[sg.HorizontalSeparator()]]
        
        layout_l = welcome_panel + [[sg.Button("My Portfolio",k='-GOTOPORTFOLIO2-'),sg.Button("Buy/Sell Crypto",k="-GOTOPURCHASE2-")]]

        #layout = [[sg.Column(layout_l, element_justification = "center"),sg.Column(layout_r,element_justification = "center",scrollable=False)]]
        return layout_l
    