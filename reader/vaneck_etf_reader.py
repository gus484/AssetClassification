import os
from datetime import datetime
from locale import atof

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily


class VanEckEtfReader(EtfReader):
    REGEX = r'[A-Z]{4}\_(\w+)\_(\d{8})\.(xlsx)'

    def __init__(self, fpath):
        super().__init__(fpath)
        self.fund_family = FundFamily.VANECK.value
        self.last_update = ''
        self.start_row = 4
        self.name_col = 2
        self.ticker_col = 3
        self.region_col = 3
        self.weight_col = 7
        self.file_name = os.path.basename(self.fpath)
        self.read_sheet_from_wb()

    def read_asset(self):
        self.file_name = self.file_name.split("_")[0]
        last_update = self.sheet.cell(1, 1).value
        last_update = last_update.split(" ")[3]

        date_format = '%m.%d.%Y'
        date_obj = datetime.strptime(last_update, date_format)
        last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, self.file_name)
        name = EtfReader.get_name_from_isin(self.fund_family, self.isin)
        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.sheet.max_row):
            name = self.sheet.cell(i, self.name_col).value
            if name is None:
                break
            weight = self.sheet.cell(i, self.weight_col).value
            weight = atof(weight.replace("%", "").replace("\xa0", ""))
            ticker = self.sheet.cell(i, self.ticker_col).value
            region = self.sheet.cell(i, self.region_col).value
            region = region.split(" ")[1]
            region = EtfReader.get_region_code(FundFamily.VANGUARD.value, region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
