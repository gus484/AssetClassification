from unittest import TestCase

from reader.ishares_etf_reader import ISharesEtfReader
from test.test_basics import create_reader


class TestIsharesEtfReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file1 = 'IWLE_holdings.csv'

    def test_reader_regex(self):
        reader = create_reader(self.test_file1)
        self.assertEqual(type(reader), ISharesEtfReader)

    def test_read_sheet(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))

    def test_read_asset(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        self.assertEqual('iShares Core MSCI World UCITS ETF', reader.asset.name)
        self.assertEqual('IE00BKBF6H24', reader.asset.isin)
        self.assertEqual('01.09.2023', reader.asset.last_history_date)
