from dataclasses import dataclass
from typing import List

@dataclass
class Trade:
    qty: int
    price: float

    @property
    def total_price(self):
        return self.volume * self.price
    
    @property
    def volume(self):
        if self.qty > 0:
            return self.qty
        else:
            return -self.qty

class FIFO:
    def __init__(self):
        self.buy_list: List[Trade] = []
        self.sell_list: List[Trade] = []
        self.pnl: float = 0.0
    
    def __repr__(self):
        return f"""
            buy_list: {self.buy_list} 
            sell_list: {self.sell_list}
            pnl: {self.pnl}
        """
    
    def add_trade(self, trade: Trade):
        if trade.qty > 0:
            if len(self.sell_list) == 0:
                self.buy_list.append(trade)
            else:
                self.cross_trade(trade)
        else:
            if len(self.buy_list) == 0:
                self.sell_list.append(trade)
            else:
                self.cross_trade(trade)

    # TODO: clean code
    def cross_trade(self, trade):
        i = -1
        if trade.qty > 0:
            for sell in self.sell_list:
                i += 1
                if trade.volume < sell.volume:
                    self.pnl += sell.price * trade.volume - trade.price * trade.volume
                    remain_volume = sell.volume - trade.volume
                    self.sell_list[i] = Trade(-remain_volume, sell.price)
                    trade = None
                    break
                else: #  buy.volume >= sell.volume
                    self.pnl += sell.price * sell.volume - trade.price * sell.volume
                    remain_volume = trade.volume - sell.volume
                    self.sell_list[i] = Trade(0, sell.price)
                    if remain_volume == 0:
                        trade = None
                    else:
                        trade = Trade(remain_volume, trade.price)
            self.sell_list = list(filter(lambda x: x.volume > 0, self.sell_list))
            if trade is not None:
                self.buy_list.append(trade)
        else:
            for buy in self.buy_list:
                i += 1
                if trade.volume < buy.volume:
                    self.pnl += trade.price * trade.volume - buy.price * trade.volume
                    remain_volume = buy.volume - trade.volume
                    self.buy_list[i] = Trade(remain_volume, buy.price)
                    trade = None
                    break
                else: #  trade.volume >= buy.volume
                    self.pnl += trade.price * buy.volume - buy.price * buy.volume
                    remain_volume = trade.volume - buy.volume
                    self.buy_list[i] = Trade(0, buy.price)
                    if remain_volume == 0:
                        trade = None
                    else:
                        trade = Trade(-remain_volume, trade.price)
            self.buy_list = list(filter(lambda x: x.volume > 0, self.buy_list))
            if trade is not None:
                self.sell_list.append(trade)

    def avg_buy_price(self):
        s = 0
        volume = 0
        for buy in self.buy_list:
            s += buy.total_price
            volume += buy.volume
        return s / volume

    def avg_sell_price(self):
        s = 0
        volume = 0
        for sell in self.sell_list:
            s += sell.total_price
            volume += sell.volume
        return s / volume


trade1 = Trade(100, 100)
trade2 = Trade(200, 200)
trade3 = Trade(300, 300)
trade4 = Trade(-500, 500)

fifo = FIFO()
fifo.add_trade(trade1)
fifo.add_trade(trade2)
fifo.add_trade(trade3)
fifo.add_trade(trade4)
print(fifo.pnl)