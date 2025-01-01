from polygon import RESTClient

class PolygonAPIBase:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.clients = [RESTClient(api_key=api_key) for api_key in api_keys]

