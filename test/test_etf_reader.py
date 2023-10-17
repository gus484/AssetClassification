from unittest import TestCase

from reader.asset import Asset
from reader.etf_reader import EtfReader, FundFamily


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
        isin = reader.get_isin_from_file_name(FundFamily.ISHARES.value, "EIMU_holdings.csv")
        self.assertEqual("IE00BD45KH83", isin)

        isin_not_exist = reader.get_isin_from_file_name(FundFamily.ISHARES.value, "ABC.csv")
        self.assertEqual(EtfReader.NOT_EXIST, isin_not_exist)

    def test_get_name_from_isin(self):
        reader = EtfReader(r"not\existing")
        name = reader.get_name_from_isin(FundFamily.ISHARES.value, "IE00BD45KH83")
        self.assertEqual("iShares Core MSCI Emerging Markets IMI UCITS ETF", name)

        name_not_exist = reader.get_name_from_isin(FundFamily.ISHARES.value, "ABC")
        self.assertEqual(EtfReader.NOT_EXIST, name_not_exist)

    def test_read_json(self):
        reader = EtfReader(r"not\existing")
        json = reader.read_json(r"not\existing")
        self.assertEqual(json, {})

    def test_get_region_code(self):
        reader = EtfReader(r"not\existing")
        code = reader.get_region_code(FundFamily.ISHARES.value, "Spanien")
        self.assertEqual("ESP", code)
