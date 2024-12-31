from polygon import RESTClient

class PolygonAPI:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.clients = [RESTClient(api_key=api_key) for api_key in api_keys]

    def get_previous_close(self, ticker):
        client = self.clients[0]
        aggs = client.get_previous_close_agg(ticker)
        return aggs[0].close