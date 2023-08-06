# Importing external libraries
import unittest

# Importing libraries we want to test
from tests import Tests

class TestKrakenLive(unittest.TestCase):

    def setUp(self):

        self.tests = Tests()

    def test_ticker(self):

        self.tests.ticker('kraken', ['XBT/USD'], ['XBT/USD'], False, 5)

    def test_ticker_multiple_pairs(self):

        self.tests.ticker('kraken', ['XBT/USD', 'SOL/USD', 'LTC/USD'], ['XBT/USD', 'SOL/USD', 'LTC/USD'], False, 8)

    def test_trade(self):

        self.tests.trade('kraken', ['XBT/USD'], ['XBT/USD'], False, 5)

    def test_trade_multiple_pairs(self):

        self.tests.trade('kraken', ['XBT/USD', 'SOL/USD', 'LTC/USD'], ['XBT/USD', 'SOL/USD', 'LTC/USD'], False, 8)

    def test_book(self):

        self.tests.book('kraken', ['XBT/USD'], ['XBT/USD'], False, 5)

    def test_book_multiple_pairs(self):

        self.tests.book('kraken', ['XBT/USD', 'SOL/USD', 'LTC/USD'], ['XBT/USD', 'SOL/USD', 'LTC/USD'], False, 8)

if __name__ == "__main__":
    unittest.main()