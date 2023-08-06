from src.testlab_sdk_python.Client import Client

class Config:
    def __init__(self, server_address, interval):
        self.server_address = server_address
        self.interval = interval

    def connect(self):
        client = Client(self)
        client.start_in_background()
        client.add_default_context()
        return client