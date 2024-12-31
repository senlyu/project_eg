from datetime import datetime, timedelta

class MarketData:
    def __init__(self, storage, query):
        self.storage = storage
        self.query = query

    def get_previous_close(self, ticker):
        yesterday = datetime.today().date() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")  
        close_price = self.storage.get_price(yesterday_str, ticker)
        if close_price is not None:
            return close_price

        price = self.query.get_previous_close(ticker)
        self.storage.add_price(yesterday_str, ticker, price)
        return price