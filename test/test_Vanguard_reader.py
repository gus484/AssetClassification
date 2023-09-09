import os
from unittest import TestCase

from reader.asset import Asset
from reader.etf_reader import EtfReader, FundFamily
from reader.vanguard_etf_reader import VanguardEtfReader


class TestVanguardEtfReader(TestCase):
    def create_reader(self) -> EtfReader:
        file = os.path.join(os.path.dirname(__file__),'data/Vanguard FTSE All-World UCITS ETF.xlsx')
        reader = VanguardEtfReader(file)
        return reader

    def test_read_sheet(self):
        reader = self.create_reader()
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))
    
    def test_read_asset(self):
        reader = self.create_reader()
        reader.read_asset()
        self.assertEqual('Vanguard FTSE All-World UCITS ETF (USD) Accumulating', reader.asset.name)
        self.assertEqual('IE00BK5BQT80', reader.asset.isin)
        self.assertEqual('31.05.2023', reader.asset.last_history_date)


