import os
from unittest import TestCase

from reader.asset import Asset
from reader.etf_reader import EtfReader, FundFamily
from reader.ishares_etf_reader import ISharesEtfReader
from reader.vanguard_etf_reader import VanguardEtfReader


class TestIsharesEtfReader(TestCase):
    def create_reader(self) -> EtfReader:
        file = os.path.join(os.path.dirname(__file__),'data/IWLE_holdings.csv')
        reader = ISharesEtfReader(file)
        return reader

    def test_read_sheet(self):
        reader = self.create_reader()
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))

    def test_read_asset(self):
        reader = self.create_reader()
        reader.read_asset()
        self.assertEqual('iShares Core MSCI World UCITS ETF', reader.asset.name)
        self.assertEqual('IE00BKBF6H24', reader.asset.isin)
        self.assertEqual('01.09.2023', reader.asset.last_history_date)
