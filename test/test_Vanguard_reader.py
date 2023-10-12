from unittest import TestCase

from reader.vanguard_etf_reader import VanguardEtfReader
from test.test_basics import create_reader


class TestVanguardEtfReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file1 = 'Aufschlüsselung der Positionen - Vanguard FTSE All-World High Dividend Yield UCITS ETF (USD) Distributing - 27.9.2023.xlsx'

    def test_reader_regex(self):
        reader = create_reader(self.test_file1)
        self.assertEqual(type(reader), VanguardEtfReader)

    def test_read_sheet(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))

    def test_read_asset(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        self.assertEqual('Vanguard FTSE All-World UCITS ETF (USD) Accumulating', reader.asset.name)
        self.assertEqual('IE00BK5BQT80', reader.asset.isin)
        self.assertEqual('31.05.2023', reader.asset.last_history_date)
