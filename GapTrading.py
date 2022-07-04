from tkinter import EXCEPTION
from matplotlib import ticker
from sqlalchemy import true
import yfinance as yf
import yahoo_fin.stock_info as si
from datetime import date,timedelta,datetime
import datetime
from yahoo_fin.stock_info import get_data
import pandas as pd
import time
import sys
from threading import Thread

from TickerDocument import TickerDocument  

class GapTrading: 
                     
    def get_gap_prices(self, ticker):  # gives an array that has the tickers name [0], lowest price vorgestern [1], highest price gestern [2]
        
        #day_of_week = datetime.datetime.today().weekday()
        #if day_of_week == 6:
         #   gestern = date.today() - timedelta(days =2)
          #  vorgestern = date.today()- timedelta(days =3)
        #elif day_of_week == 0:
         #   gestern = date.today() - timedelta(days =3)
          #  vorgestern = date.today()- timedelta(days =4)
        #elif day_of_week == 1:
         #   gestern = date.today() - timedelta(days =1)
          #  vorgestern = date.today()- timedelta(days =4)
        #else:
         #   gestern = date.today() - timedelta(days =1)
          #  vorgestern = date.today()- timedelta(days =2)
            
        
        #d2 = gestern.strftime("%d/%m/%Y")
        #d1 = vorgestern.strftime("%d/%m/%Y")
        
        
        try:
            msft = yf.Ticker(ticker)
            ticker_data = msft.history(period="2d")
            #ticker_data= get_data(ticker, start_date=str(d1), end_date=str(d2), index_as_date = True, interval="1d")
            df = pd.DataFrame(ticker_data)
            if len(df) >= 2 :
                priceArray = ticker , float(df.iat[0,2]),  float(df.iat[1,1])
            else:
                print(df)
                priceArray = ticker, 0, 0
        except Exception as e:
            priceArray = ticker , 0,0 
            print(e)
        
        print(priceArray)
        #print (df)
        return priceArray
    
    
    def get_price(self,ticker):
        stock = yf.Ticker(ticker)
        price = stock.info['regularMarketPrice']
        return price
    
    def get_tickers_with_gap(self,array_with_tickers):
        array_with_gap = []
        
        
        
        i = 0
        for ticker in array_with_tickers:
            if self.analyze_gap_price(self.get_gap_prices(ticker)) == True:
                array_with_gap.append(ticker)
                print(array_with_gap)
        return array_with_gap
            
            
    
    def analyze_gap_price(self,price_array):
        if float(price_array[1]) > float(price_array [2]):
            return True
        else:
            return False
    
    
        
#gp = GapTrading()
#td = TickerDocument()
#td.get_tickers_to_doc()
#print (gp.get_price("TSLA"))
#print(gp.get_tickers_with_gap(td.doc_to_list()))
