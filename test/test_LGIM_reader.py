from unittest import TestCase

from reader.lgim_etf_reader import LGIMEtfReader
from test.test_basics import create_reader


class TestLgimEtfReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file1 = 'Fund-holdings_LG-Gerd-Kommer-Multifactor-Equity-UCITS-ETF-Gerd-Kommer-Multifactor-Equity-UCITS-ETF-USD-Acc_26-01-2024.csv'

    def test_reader_regex(self):
        reader = create_reader(self.test_file1)
        self.assertEqual(type(reader), LGIMEtfReader)

    def test_read_sheet(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))

    def test_read_asset(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        self.assertEqual('L&G Gerd Kommer Multifactor Equity UCITS ETF - USD Accumulating ETF', reader.asset.name)
        self.assertEqual('IE0001UQQ933', reader.asset.isin)
        self.assertEqual('25.01.2024', reader.asset.last_history_date)
