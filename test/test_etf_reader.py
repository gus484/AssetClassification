import os
from unittest import TestCase

from reader.asset import Asset
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class TestEtfReader(TestCase):
    def test_update_region(self):
        reader = EtfReader(r"not\existing")
        reader.asset = Asset('abc', '123', 0.0, '', [])
        reader.update_region('region1', 5.0)
        self.assertEqual(5.0, reader.asset.regions['region1'].weight)

        reader.update_region('region1', 3.0)
        self.assertEqual(8.0, reader.asset.regions['region1'].weight)

    def test_read_sheet_from_wb(self):
        reader = EtfReader(r"not\existing")
        reader.read_sheet_from_wb()
        self.assertIsNone(reader.sheet)

    def test_get_isin_from_file_name(self):
        reader = EtfReader(r"not\existing")
        isin = reader.get_isin_from_file_name(FundFamily.ISHARES, "EIMU_holdings.csv")
        self.assertEqual("IE00BD45KH83", isin)

        isin_not_exist = reader.get_isin_from_file_name(FundFamily.ISHARES, "ABC.csv")
        self.assertEqual(EtfReader.NOT_EXIST, isin_not_exist)

    def test_get_name_from_isin(self):
        reader = EtfReader(r"not\existing")
        name = reader.get_name_from_isin(FundFamily.ISHARES, "IE00BD45KH83")
        self.assertEqual("iShares Core MSCI Emerging Markets IMI UCITS ETF", name)

        name_not_exist = reader.get_name_from_isin(FundFamily.ISHARES, "ABC")
        self.assertEqual(EtfReader.NOT_EXIST, name_not_exist)

    def test_get_default_isin(self):
        reader = EtfReader(r"not\existing")
        isin = reader.get_isin()
        self.assertEqual("XX0000000010", isin)

    def test_get_default_name(self):
        reader = EtfReader(r"not\existing")
        reader.fund_family = FundFamily.ISHARES
        name = reader.get_name()
        self.assertEqual("ISHARES ETF01", name)

    def test_wrong_config(self):
        file = os.path.join(os.path.dirname(__file__), f'data/dummy_etf.csv')
        print(file)
        reader = EtfReader(file)
        reader.read_asset()

    def test_read_json(self):
        reader = EtfReader(r"not\existing")
        json = reader.read_json(r"not\existing")
        self.assertEqual(json, {})

    def test_get_region_code(self):
        reader = EtfReader(r"not\existing")
        code_de_full = reader.get_region_code(LocationCodes.DE_FULL_NAME, "Spanien")
        code_en_full = reader.get_region_code(LocationCodes.EN_FULL_NAME, "Spain")
        code_alpha_2 = reader.get_region_code(LocationCodes.ALPHA_2_CODE, "ES")
        self.assertEqual("ESP", code_de_full)
        self.assertEqual("ESP", code_en_full)
        self.assertEqual("ESP", code_alpha_2)
