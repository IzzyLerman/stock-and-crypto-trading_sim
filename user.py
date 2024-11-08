class MarketCoin:
    def __init__(self) -> None:
        pass
    
    def __init__(self, name, price, market_cap,symbol ,percent_change_24h, percent_change_7d):
        self.name = name
        self.price = price
        self.market_cap = market_cap
        self.symbol = symbol
        self.percent_change_24h = percent_change_24h
        self.percent_change_7d = percent_change_7d
class UserCoin:
    def __init__(self) -> None:
        self.quantity = 0
    
    def __init__(self, coin, quantity):
        self.quantity = quantity
        self.name = coin.name
        self.price = coin.price
        self.market_cap = coin.market_cap
        self.symbol = coin.symbol
        self.percent_change_24h = coin.percent_change_24h
        self.percent_change_7d = coin.percent_change_7d
    def update_quantity(self, diff):
        self.quantity += diff

class User:
    def __init__(self) -> None:
        self.bankroll = 0

    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.starting_bankroll = bankroll
        self.portfolio = []

    #Purchase a market coin;-4 if selling last of coins, return -3 if not enough to sell, -2 if not enough money, -1 if existing coin, index of coin if its a new coin, along with second value which
    # is true if we are selling the last of a user's stock
    def purchase(self,coin,quantity,mode)->int:
        cost = coin.price * quantity
        if(mode == 'Buy'):
            if cost > self.bankroll:
                return -2, False
            for c in self.portfolio:
                if c.name == coin.name:
                    c.quantity += quantity
                    self.bankroll -= cost
                    return -1, False
            self.portfolio.append(UserCoin(coin, quantity))
            self.bankroll -= cost
            return len(self.portfolio)-1, False
        else:
            for idx,c in enumerate(self.portfolio):
                if c.name == coin.name:
                    if c.quantity < quantity:
                        return -3, False
                    else:
                        quantity *= -1
                        c.quantity += quantity
                        if c.quantity == 0:
                            self.portfolio.pop(idx)
                        self.bankroll += cost
                        return (-1, False) if c.quantity > 0 else (idx, True)
            return -3, False




    
    #return a usercoin that corresponds to the given marketcoin (if it exists in user's portfolio)
    def get_coin(self, coin) -> UserCoin:
        for c in self.portfolio:
            if c.name == coin.name:
                return c
        return None

    def portfolio_value(self):
        return self.bankroll + sum((c.quantity * c.price for c in self.portfolio))
    
    def portfolio_value_percent(self):
        return self.portfolio_value()-self.starting_bankroll / self.starting_bankroll
    
    def net_diff(self):
        return self.portfolio_value() - self.starting_bankroll
        
    def net_diff_percent(self):
        return self.net_diff()/self.starting_bankroll 

    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(f'{self.name}\n')
            f.write(f'{self.bankroll}\n')
            f.write(f'{self.starting_bankroll}\n')
            f.write(f'{len(self.portfolio)}\n')
            for c in self.portfolio:
                f.write(f'{c.quantity}\n')
                f.write(f'{c.name}\n')
                f.write(f'{c.price}\n')
                f.write(f'{c.market_cap}\n')
                f.write(f'{c.symbol}\n')
                f.write(f'{c.percent_change_24h}\n')
                f.write(f'{c.percent_change_7d}\n')
                

