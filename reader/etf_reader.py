import abc
import json
import locale
import logging
import os.path
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from pathlib import Path

import dateparser
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from report.region import Region

try:
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
except locale.Error as e:
    print("Could not load local 'de_DE.utf8'")

log = logging.getLogger("ac")


class FundFamily(Enum):
    ISHARES = 'ISHARES'
    LGIM = "LGIM"
    SPDR = "SPDR"
    VANECK = 'VANECK'
    VANGUARD = 'VANGUARD'


class EtfReader:
    NAME_COUNTER = 0
    ISIN_COUNTER = 0
    ISIN_LOOKUP = None
    ISIN_TO_NAME_LOOKUP = None
    NOT_EXIST = '----'
    REGION_MAPPING = {}

    def __init__(self, fpath: str):
        self.name = ''
        self.fpath = fpath
        self.asset = None
        self.sheet = None
        self.values = []
        self.isin = ''
        self.fund_family = None

    def update_region(self, region: str, weight: float) -> None:
        if region not in self.asset.regions:
            self.asset.regions[region] = Region(region, weight, 1)
        else:
            self.asset.regions[region].weight += weight
            self.asset.regions[region].num_of_countries += 1

    def read_sheet_from_wb(self):
        try:
            wb = load_workbook(filename=self.fpath)
            self.sheet = wb.active
        except InvalidFileException as e:
            log.error(f"Could not read file: {self.fpath}")

    def parse_date(self, last_update: str, date_formats: list[str] = None) -> datetime:
        try:
            date_obj = dateparser.parse(last_update, date_formats=date_formats)
            return date_obj
        except ValueError:
            return datetime.now()

    @staticmethod
    def get_isin_from_file_name(fund_family, name) -> str:
        if EtfReader.ISIN_LOOKUP is None:
            path_to_mapping = Path(__file__).parent
            path_to_mapping = os.path.join(path_to_mapping, "../", "mappings", "isin_lookup.json")
            EtfReader.ISIN_LOOKUP = EtfReader.read_json(path_to_mapping)
        return EtfReader.ISIN_LOOKUP.get(fund_family, {}).get(name, EtfReader.NOT_EXIST)

    @staticmethod
    def get_name_from_isin(fund_family, isin) -> str:
        if EtfReader.ISIN_TO_NAME_LOOKUP is None:
            path_to_mapping = Path(__file__).parent
            path_to_mapping = os.path.join(path_to_mapping, "../", "mappings", "isin_to_name_lookup.json")
            EtfReader.ISIN_TO_NAME_LOOKUP = EtfReader.read_json(path_to_mapping)
        return EtfReader.ISIN_TO_NAME_LOOKUP.get(fund_family, {}).get(isin, EtfReader.NOT_EXIST)

    @staticmethod
    def get_isin_and_names():
        # pre load lookup files
        EtfReader.get_name_from_isin(FundFamily.VANGUARD, '')
        EtfReader.get_isin_from_file_name(FundFamily.VANGUARD, '')

        etf_data = EtfReader.ISIN_TO_NAME_LOOKUP
        for issuer, data in EtfReader.ISIN_LOOKUP.items():
            if issuer in etf_data:
                continue

            etf_data[issuer] = {}
            for name, isin in data.items():
                etf_data[issuer][isin] = name

        return etf_data

    @staticmethod
    def read_json(path: str):
        if not os.path.exists(path):
            log.warning(f"No region mapping found:{path}")
            return {}

        with open(path, 'r', encoding="utf-8") as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                log.error(f"Could not read region mapping for: {path}")
                return {}

    @staticmethod
    def get_region_code(fund_family, name):
        if fund_family not in EtfReader.REGION_MAPPING:
            path_to_mapping = Path(__file__).parent
            path_to_mapping = os.path.join(path_to_mapping, "../", "mappings", fund_family + ".json")
            EtfReader.REGION_MAPPING[fund_family] = EtfReader.read_json(path_to_mapping)
        return EtfReader.REGION_MAPPING[fund_family].get(name, name)

    def set_default_isin(self):
        EtfReader.ISIN_COUNTER += 1
        self.isin = f'XX{EtfReader.ISIN_COUNTER:09d}0'
        self.asset.isin = self.isin

    def set_default_name(self):
        EtfReader.NAME_COUNTER += 1
        self.name = f'{self.fund_family}ETF{EtfReader.NAME_COUNTER:02d}'
        self.asset.name = self.name

    @abc.abstractmethod
    def read_sheet(self):
        """Method documentation"""
        return

    @abc.abstractmethod
    def read_asset(self):
        """Method documentation"""
        return
