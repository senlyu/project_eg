from datetime import datetime, timedelta
import pytz
from src.market_data.polygon_apis.previous_close import PolygonAPIClosePrice
import asyncio

class MarketDataBase:
    def __init__(self, storage):
        self.storage = storage

    async def get_previous_close_for_one_ticker(self, ticker):
        nyc_timezone = pytz.timezone('America/New_York') 
        yesterday = datetime.now(nyc_timezone).date() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")  

        close_price = self.storage.get_price(yesterday_str, ticker)
        if close_price is not None:
            f = asyncio.Future()
            await self.set_future(f, close_price)
            return f

        f = asyncio.Future()
        price = await self.query_previous_close(ticker)
        self.storage.add_price(yesterday_str, ticker, round(price, 2))
        await self.set_future(f, price)
        return f

    async def get_previous_close_for_multiple_tickers(self, tickers):
        t = []
        for ticker in tickers:
            if any(char.isdigit() for char in ticker):
                ticker = "O:" + ticker
            t.append(await self.get_previous_close_for_one_ticker(ticker))
        await asyncio.gather(*t)

        res = {}
        for i in range(len(tickers)):
            ticker = tickers[i]
            res[ticker] = round(float(t[i].result()), 2)
        return res

    def get_previous_close(self, tickers):
        return asyncio.run(self.get_previous_close_for_multiple_tickers(tickers))

    def query_previous_close(self, ticker):
        pass

    async def set_future(self, future, value):
        future.set_result(value)


class MarketDataWithPolygon(MarketDataBase):
    def __init__(self, storage, polygon_settings):
        super().__init__(storage)

        polygon_api_keys = polygon_settings.get('api_keys')
        self.query_previous_close_api = PolygonAPIClosePrice(polygon_api_keys, len(polygon_api_keys), 5)

    def query_previous_close(self, ticker):
        return self.query_previous_close_api.query_by_limit(ticker)

