# Importing external libraries
import unittest

# Importing libraries we want to test
from tests import Tests

class TestBitfinexLive(unittest.TestCase):

    def setUp(self):

        self.tests = Tests()

    def test_ticker(self):

        self.tests.ticker('bitfinex', ['BTCUSD'], ['tBTCUSD'], False, 5)

    def test_ticker_multiple_pairs(self):

        self.tests.ticker('bitfinex', ['BTCUSD', 'LTCUSD', 'ETHUSD'], ['tBTCUSD', 'tLTCUSD', 'tETHUSD'], False, 8)

    def test_trade(self):

        self.tests.trade('bitfinex', ['BTCUSD'], ['tBTCUSD'], False, 5)

    def test_trade_multiple_pairs(self):

        self.tests.trade('bitfinex', ['BTCUSD', 'LTCUSD', 'ETHUSD'], ['tBTCUSD', 'tLTCUSD', 'tETHUSD'], False, 8)

    def test_book(self):

        self.tests.book('bitfinex', ['BTCUSD'], ['tBTCUSD'], False, 5)

    def test_book_multiple_pairs(self):

        self.tests.book('bitfinex', ['BTCUSD', 'LTCUSD', 'ETHUSD'], ['tBTCUSD', 'tLTCUSD', 'tETHUSD'], False, 8)

if __name__ == "__main__":
    unittest.main()