from unittest import TestCase

from reader.vaneck_etf_reader import VanEckEtfReader
from test.test_basics import create_reader


class TestVaneckEtfReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file1 = 'TDIV_Stand_20230511.xlsx'

    def test_reader_regex(self):
        reader = create_reader(self.test_file1)
        self.assertEqual(type(reader), VanEckEtfReader)

    def test_read_sheet(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))

    def test_read_asset(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        self.assertEqual('VanEck Morningstar Developed Markets Dividend Leaders UCITS ETF', reader.asset.name)
        self.assertEqual('NL0011683594', reader.asset.isin)
        self.assertEqual('11.05.2023', reader.asset.last_history_date)
