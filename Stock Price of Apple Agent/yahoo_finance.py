import yfinance as yf
import json

def get_stock_price(ticker_symbol: str)-> str:
    """Fetch the current price of the stck given its ticker symbol"""
    try:
        stock = yf.Ticker(ticker_symbol.upper())
        # current_price = stock.fast_info('last price')
        price = stock.fast_info['last_price']
        currency = stock.fast_info['currency']
        return json.dumps({
            "ticker":ticker_symbol.upper(),
            "price":price,
            "currency":currency
        })
    except Exception as e:
        print(f"Error fetching stock price for {ticker_symbol}: {e}")  
        return json.dumps({
            "error":str(e)
        })
    
if __name__ == "__main__":
    # res= get_stock_price('AAPL') #APPLE 
    res= get_stock_price('TSLA')   #TESLA
    print(res)