# Importing internal libraries
from .spot.live.live import Live
from .symbols.symbols import Symbols
from .storage.storage import Storage



class GoQuant():

    def __init__(self):

        # Connecting to API V2
        self.__tenant_live_url = 'wss://api.goquant.io/ws'
        # self.static = Static(self.__tenant_historical_url)
        # TODO: Integrate Historical data

        self.live = Live(self.__tenant_live_url)
        self.symbols = Symbols()
        self.storage = Storage()