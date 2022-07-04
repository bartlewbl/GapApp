
import yfinance as yf
import yahoo_fin.stock_info
import yahoo_fin.stock_info as si
import time


class TickerDocument:
    
    #def __init__ (self):
        
    def get_tickers_to_doc(self):
        tickers = yahoo_fin.stock_info.tickers_nasdaq()
        file = open("Nasdaq_Tickers.txt","r+")
        file.truncate(0)
        for x in tickers:
            try:
                volume = si.get_quote_table(x)["Volume"]
                #time.sleep(1)
            except:
                volume = 0
            print(x + "  "+str(volume))
            if volume > 150000:
                file.write(x)
                file.write(" ")
    
    def doc_to_list(self):
        file = open("Nasdaq_Tickers.txt")
        tickers = file.read().split()
        #print(tickers) 
        return tickers
    
    

#ticDoc = TickerDocument()
#ticDoc.get_tickers_to_doc()
#ticDoc.doc_to_list()