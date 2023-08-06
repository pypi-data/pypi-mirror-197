# Importing external libraries
import unittest

# Importing libraries we want to test
from tests import Tests

class TestBinanceLive(unittest.TestCase):

    def setUp(self):

        self.tests = Tests()

    def test_ticker(self):

        self.tests.ticker('binance', ['btcusdt'], ['BTCUSDT'], False, 5)

    def test_ticker_multiple_pairs(self):

        self.tests.ticker('binance', ['btcusdt', 'ethbtc', 'ltcbtc'], ['BTCUSDT', 'ETHBTC', 'LTCBTC'], False, 8)

    def test_trade(self):

        self.tests.trade('binance', ['btcusdt'], ['BTCUSDT'], False, 5)

    def test_trade_multiple_pairs(self):

        self.tests.trade('binance', ['btcusdt', 'ethbtc', 'ltcbtc'], ['BTCUSDT', 'ETHBTC', 'LTCBTC'], False, 8)

    def test_book(self):

        self.tests.book('binance', ['btcusdt'], ['BTCUSDT'], False, 5)

    def test_book_multiple_pairs(self):

        self.tests.book('binance', ['btcusdt', 'ethbtc', 'ltcbtc'], ['BTCUSDT', 'ETHBTC', 'LTCBTC'], False, 8)

if __name__ == "__main__":
    unittest.main()