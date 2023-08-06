from Client import Client

class Config:
    def __init__(self, server_address, interval):
        self.server_address = server_address
        self.interval = interval

    def connect(self):
        client = Client(self)
        client.fetch_features()
        client.add_default_context()
        client.start_in_background()
        return client