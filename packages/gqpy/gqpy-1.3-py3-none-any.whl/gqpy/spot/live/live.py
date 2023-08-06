# Importing internal functionality
from .handler import handle_live_data

class Live:

    def __init__(self, url):
        self.url = url
        self.__supported_exchanges = ['binance', 'bitinfex', 'coinbase', 'kraken']

    # By default, output will be printed, the WS will run indefinitely and it will not be stored anywhere
    def book(self, exchange_name, symbol_pair, print=True, run_time=True, storage_obj=None):
        return handle_live_data(self.url, exchange_name, symbol_pair, print, run_time, 'book', storage_obj)

    def ticker(self, exchange_name, symbol_pair, print=True, run_time=True, storage_obj=None):
        return handle_live_data(self.url, exchange_name, symbol_pair, print, run_time, 'ticker', storage_obj)

    def trade(self, exchange_name, symbol_pair, print=True, run_time=True, storage_obj=None):
        return handle_live_data(self.url, exchange_name, symbol_pair, print, run_time, 'trade', storage_obj)

    def get_supported_exchanges(self):
        return self.__supported_exchanges