from unittest import TestCase

from reader.xtrackers_etf_reader import XtrackersEtfReader
from test.test_basics import create_reader


class TestXtrackerEtfReader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file1 = 'Constituent_IE00BJ0KDQ92.xlsx'

    def test_reader_regex(self):
        reader = create_reader(self.test_file1)
        self.assertEqual(type(reader), XtrackersEtfReader)

    def test_read_sheet(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        reader.read_sheet()

        self.assertEqual(8, len(reader.asset.values))

    def test_read_asset(self):
        reader = create_reader(self.test_file1)
        reader.read_asset()
        self.assertEqual('XTRACKERS ETF01', reader.asset.name)
        self.assertEqual('IE00BJ0KDQ92', reader.asset.isin)
        self.assertEqual('28.01.2024', reader.asset.last_history_date)
