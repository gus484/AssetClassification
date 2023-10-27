import os
from unittest import TestCase

from pp.pp_updater import PPUpdater


class TestPPUpdater(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.src_path = os.path.join(os.path.dirname(__file__), f'data/pp_test.xml')
        cls.target_path = os.path.join(os.path.dirname(__file__), f'out/pp_test.xml')

        if os.path.exists(cls.src_path + ".bck"):
            os.remove(cls.src_path + ".bck")

        cls.test_data = {
            'IE00B8GKDB10': {
                'DW Amerika': [['DW Amerika', '46.09', 192], [['USA', '42.28', 162], ['Kanada', '3.81', 30]]]},
            'NL0011683594': {'DW Amerika': [['DW Amerika', '32.50', 16], [['USA', '22.76', 8], ['Kanada', '9.74', 8]]],
                             'DW Europa/Naher Osten': [['DW Europa/Naher Osten', '52.85', 39],
                                                       [['Frankreich', '12.86', 6], ['Großbritannien', '8.15', 5],
                                                        ['Deutschland', '11.77', 6], ['Italien', '5.67', 5],
                                                        ['Schweiz', '4.60', 4], ['Spanien', '2.02', 2],
                                                        ['Finnland', '1.28', 0], ['Schweden', '3.04', 5],
                                                        ['Belgien', '0.87', 1], ['Niederlande', '0.50', 0],
                                                        ['Norwegen', '1.20', 3], ['Österreich', '0.55', 1],
                                                        ['Israel', '0.34', 1]]],
                             'DW Asien/Pazifik': [['DW Asien/Pazifik', '12.33', 22],
                                                  [['Japan', '7.04', 16], ['Australien', '1.54', 1],
                                                   ['Singapur', '3.02', 4], ['Hongkong', '0.73', 1]]],
                             'Welt': [['Welt', '1.26', 1], [['Kaimaninseln', '0.94', 1], ['Bermuda', '0.32', 0]]],
                             'EM Europa/Naher Osten': [['EM Europa/Naher Osten', '0.27', 0], [['Polen', '0.27', 0]]]}

        }

    def test_read_securities(self):
        updater = PPUpdater(self.src_path, self.target_path)
        updater.read_pp_securities()
        self.assertEqual(3, len(updater.securities))
        self.assertIn("IE00B53SZB19", updater.securities.keys())
        self.assertIn("NL0011683594", updater.securities.keys())
        self.assertIn("IE00B8GKDB10", updater.securities.keys())
        self.assertNotIn("IE0001UQQ933", updater.securities.keys())

    def test_backup(self):
        backup_path = self.src_path + ".bck"
        updater = PPUpdater(self.src_path, self.target_path)

        self.assertFalse(os.path.exists(backup_path))
        updater.create_backup()
        self.assertTrue(os.path.exists(backup_path))

    def test_exist_taxonomy(self):
        backup_path = self.src_path + ".bck"
        updater = PPUpdater(self.src_path, self.target_path)

        self.assertTrue(updater.exist_taxonomy("Regionen (GPO)"))
        self.assertFalse(updater.exist_taxonomy("Foo"))

    def test_full(self):
        return
        pp_updater = PPUpdater(self.src_path, self.target_path)
        pp_updater.run(self.test_data, "ETFClassification")
