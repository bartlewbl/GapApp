from ibapi.client import EClient
from ibapi.wrapper import EWrapper 
from ibapi.contract import Contract
from ibapi.order import *
import time
from threading import Thread

from numpy import short

from GapTrading import GapTrading
from TickerDocument import TickerDocument


class TWS(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self,self)
        
        
      
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextId = orderId
        print("Next valid id:", self.nextId)
        
    def createContract(self,symbol,sec_type,exchange,currency):
        contract = Contract()
        contract.symbol = str(symbol)
        contract.secType = str(sec_type)
        contract.exchange = str(exchange)
        contract.currency = str(currency)
        return contract
    
    def createOrder (self):
        order = Order()
        order.action = 'SELL'
        order.totalQuantity = 1
        order.orderType = 'MKT'
        #order.lmtPrice = '1.10'
        order.orderId = self.nextId
        self.nextId += 1
        return order
    
    def createShortOrder(self):
        stop_order = Order()
        stop_order.action = 'BUY'
        stop_order.totalQuantity = 1
        stop_order.orderType = 'TRAIL'
        stop_order.trailingPercent = 5
        stop_order.orderId = self.nextId
        self.nextId += 1
        return stop_order
    
    def connect_TWS(self):
        self.connect('127.0.0.1', 7497, 1)
        self.run()
        
    def short_tickers(self):
        gp = GapTrading()
        td = TickerDocument()
        
        array_to_short = gp.get_tickers_with_gap(td.doc_to_list())
        for ticker in array_to_short:
            #short_limit = self.create_short_limit(float(gp.get_price(ticker)))
            #print("Shorting: "+ ticker +" with take profit: " + str(short_limit))
            self.placeOrder(self.createOrder().orderId,self.createContract(ticker,"STK","SMART","USD"),self.createOrder())
            time.sleep(5)
            self.placeOrder(self.createShortOrder().orderId,self.createContract(ticker,"STK","SMART","USD"),self.createShortOrder())
            time.sleep(5)
    
    def create_short_limit(self,price):
        return 1.05 * price
        
    def run_and_commands(self):
        td = TickerDocument()
        int_thread = Thread(target=self.connect_TWS)
        int_thread.start()
        x = "Programm started!"
        
        try:
            while x != "q":
                x = input("")
                
                if x == "o":
                    gap_thread = Thread(target = self.short_tickers)
                    gap_thread.start()
                if x == "update tickers":
                    doc_thread = Thread(target = td.get_tickers_to_doc())
                    doc_thread.start()
                if x == "otest":
                    self.placeOrder(self.createOrder().orderId,self.createContract("AAPL","STK","SMART","USD"),self.createOrder())
                    time.sleep(5)
                    self.placeOrder(self.createShortOrder().orderId,self.createContract("AAPL","STK","SMART","USD"),self.createShortOrder())
                    time.sleep(5)
            self.disconnect()
            quit()
        except:
            self.disconnect()
        finally:
            quit()
        
        
    
        



       
app = TWS()
td1 = TickerDocument()

app.nextId = None
thread_2 = Thread(target=app.run_and_commands)

thread_2.start()
#time.sleep(10)
#app.placeOrder(app.createOrder().orderId,app.createContract("AAPL","STK","SMART","USD"),app.createOrder())
#print("xd")
#app.disconnect()