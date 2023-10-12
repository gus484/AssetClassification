from unittest import TestCase

from reader.spdr_etf_reader import SpdrEtfReader
from test.test_basics import create_reader


class TestSPDREtfReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file1 = 'holdings-daily-emea-en-zprg-gy.xlsx'

    def test_reader_regex(self):
        reader = create_reader(self.test_file1)
        self.assertEqual(type(reader), SpdrEtfReader)

    def test_read_sheet(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(7, len(reader.asset.values))

    def test_read_asset(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        self.assertEqual('SPDR® S&P® Global Dividend Aristocrats UCITS ETF (Dist)', reader.asset.name)
        self.assertEqual('IE00B9CQXS71', reader.asset.isin)
        self.assertEqual('25.09.2023', reader.asset.last_history_date)
