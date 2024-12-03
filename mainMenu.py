import PySimpleGUI as sg

class MainMenu:
    def setup_layout():
        welcome_panel = [[sg.Frame('',[[sg.Text("Welcome to CryptoGenius!")],
            [sg.Text("Test out your trading skills against real-time data!")],
            [sg.Text("Make some trades, then come back tomorrow to see how you would have done in the real market!")],
            [sg.Text("Trading only takes a couple clicks!")]])],[sg.HorizontalSeparator()]]
        
        return welcome_panel + [[sg.Button("My Portfolio",k='-GOTOPORTFOLIO2-'),sg.Button("Buy/Sell Crypto",k="-GOTOPURCHASE2-")]]
    