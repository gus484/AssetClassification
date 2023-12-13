import os
import re

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class XtrackersEtfReader(EtfReader):
    REGEX = r'(Constituent)\_([A-Za-z0-9]+)\.(xlsx)'

    def __init__(self, fpath: str):
        super().__init__(fpath)
        self.fund_family = FundFamily.XTRACKERS.value
        self.start_row = 5
        self.ticker_col = 1
        self.name_col = 2
        self.weight_col = 11
        self.region_col = 3
        self.read_sheet_from_wb()

    def read_asset(self):
        name = os.path.basename(self.fpath)
        last_update = self.parse_date(self.sheet.title)
        last_update = last_update.strftime('%d.%m.%Y')

        x = re.search(self.REGEX, name)
        if x is not None:
            self.isin = x[2]
        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.sheet.max_row):
            name = self.sheet.cell(i, self.name_col).value
            if name is None:
                break
            weight = self.sheet.cell(i, self.weight_col).value * 100.0
            ticker = self.sheet.cell(i, self.ticker_col).value
            region = self.sheet.cell(i, self.region_col).value
            region = EtfReader.get_region_code(LocationCodes.ALPHA_2_CODE, region[:2])
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
