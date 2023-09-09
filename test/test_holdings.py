import unittest
from unittest import TestCase
from holdings import Holdings, Position
from reader.asset import Asset, Value


class TestHoldings(TestCase):

    def create_position_data(self):
        positions = {
            'a': Position('abc', '123', 'de', {'isin1' :(0.1, 0.2), 'isin2': (0.3,0.4)}),
            'b': Position('cde', '456', 'de', {'isin2' :(0.1, 0.2), 'isin3': (0.3,0.4)})
        }
        return positions

    def create_test_data(self):
        test_data = ['abc', 'abc company', 'def', 'ghi']
        return test_data

    def create_assets(self) -> dict[str: Asset]:
        values1 = [Value("company1", 0.5, 0.5, ''), Value("bigplayer", 0.5, 0.5, '')]
        values2 = [Value("unternehmen1", 0.5, 0.5, ''), Value("company1", 0.5, 0.5, '')]

        asset1 = Asset("abc", "123", 0.0, "", values1)
        asset2 = Asset("xyz", "456", 0.0, "", values2)
        return {asset1.isin:asset1, asset2.isin:asset2}

    def test_merge_holdings(self):
        assets = self.create_assets()
        positions = Holdings.merge_holdings(assets)
        self.assertEqual(3, len(positions))

    def test_find_duplicates(self):
        test_data = self.create_test_data()

        duplicates = Holdings.find_duplicates(test_data)
        self.assertEqual(1, len(duplicates))

    @unittest.skip
    def test_remove_duplicates(self):
        duplicates = [('abc', 'abc company')]
        positions = Holdings.remove_duplicates([],duplicates)
        self.assertEqual(1, len(positions))

    def test_create_overlaps(self):
        positions = self.create_position_data()
        overlaps = Holdings.create_overlaps(positions)
        self.assertEqual(3, len(overlaps))
        self.assertEqual(1, len(overlaps['isin1']))
        self.assertEqual(2, len(overlaps['isin2']))

