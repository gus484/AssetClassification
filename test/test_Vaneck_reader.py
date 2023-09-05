import os
from unittest import TestCase

from reader.etf_reader import EtfReader
from reader.vaneck_etf_reader import VanEckEtfReader


class TestVanguardEtfReader(TestCase):
    def create_reader(self) -> EtfReader:
        file = os.path.join(os.path.dirname(__file__),'data/TDIV_Stand_20230511.xlsx')
        reader = VanEckEtfReader(file)
        return reader

    def test_read_sheet(self):
        reader = self.create_reader()
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))
    
    def test_read_asset(self):
        reader = self.create_reader()
        reader.read_asset()
        self.assertEqual('VanEck Morningstar Developed Markets Dividend Leaders UCITS ETF', reader.asset.name)
        self.assertEqual('NL0011683594', reader.asset.isin)
        self.assertEqual('11.05.2023', reader.asset.last_history_date)


