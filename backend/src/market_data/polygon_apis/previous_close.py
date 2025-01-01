
from src.market_data.polygon_api_base import PolygonAPIBase
from src.market_data.limit_query import LimitQuery

class PolygonAPIClosePrice(PolygonAPIBase, LimitQuery):

    def __init__(self, api_keys, cluster, limit, sleep_time=60):
        PolygonAPIBase.__init__(self, api_keys)
        LimitQuery.__init__(self, cluster, limit, sleep_time)


    def query(self, ticker):
        print(f"query for {ticker}")
        client = self.clients[0]
        aggs = client.get_previous_close_agg(ticker)
        return aggs[0].close