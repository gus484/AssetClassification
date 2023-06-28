import abc
import json
import locale
import logging
import os.path

from report.region import Region

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

log = logging.getLogger("__main__")


class EtfReader:
    ISIN_LOOKUP = None
    ISIN_TO_NAME_LOOKUP = None
    REGION_MAPPING = {}

    def __init__(self, sheet):
        self.name = ''
        self.isin = ''
        self.sheet = sheet
        self.asset = None
        self.values = []

    def update_region(self, region, weight):
        if region not in self.asset.regions:
            self.asset.regions[region] = Region(region, weight)
        else:
            self.asset.regions[region].weight += weight
            self.asset.regions[region].num_of_countries += 1

    @staticmethod
    def get_isin_from_file_name(fund_family, name):
        if EtfReader.ISIN_LOOKUP is None:
            EtfReader.ISIN_LOOKUP = EtfReader.read_json(os.path.join("mappings", "isin_lookup.json"))
        return EtfReader.ISIN_LOOKUP.get(fund_family, {}).get(name, '----')

    @staticmethod
    def get_name_from_isin(fund_family, isin):
        if EtfReader.ISIN_TO_NAME_LOOKUP is None:
            EtfReader.ISIN_TO_NAME_LOOKUP = EtfReader.read_json(os.path.join("mappings", "isin_to_name_lookup.json"))
        return EtfReader.ISIN_TO_NAME_LOOKUP.get(fund_family, {}).get(isin, '----')

    @staticmethod
    def read_json(path):
        if not os.path.exists(path):
            log.warning(f"No region mapping found:{path}")
            return {}

        with open(path, 'r', encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def get_region_code(fund_family, name):
        if fund_family not in EtfReader.REGION_MAPPING:
            EtfReader.REGION_MAPPING[fund_family] = EtfReader.read_json(os.path.join("mappings", fund_family + ".json"))
        return EtfReader.REGION_MAPPING[fund_family].get(name, name)

    def add_region(self, region, weight):
        if region not in self.asset.regions:
            self.asset.regions[region] = weight
        else:
            self.asset.regions[region] += weight

    @abc.abstractmethod
    def read_sheet(self):
        """Method documentation"""
        return
