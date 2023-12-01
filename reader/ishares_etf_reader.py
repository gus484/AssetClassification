import csv
import os
from locale import atof

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class ISharesEtfReader(EtfReader):
    REGEX = r'[A-Z0-9]{4}\_(holdings)\.(csv)'

    def __init__(self, fpath: str):
        super().__init__(fpath)
        self.fund_family = FundFamily.ISHARES.value
        self.start_row = 4
        self.ticker_col = 0
        self.name_col = 1
        self.weight_col = 5
        self.region_col = 9

    def read_asset(self):
        name = os.path.basename(os.path.normpath(self.fpath))
        with open(self.fpath, newline='', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:
                    last_update = line[1]

                if line_no == 3:
                    # normally there are 12 cols
                    if len(line) == 13:
                        self.weight_col += 1
                        self.region_col += 1
                    break
        date_obj = self.parse_date(last_update)
        last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, name)
        name = EtfReader.get_name_from_isin(self.fund_family, self.isin)
        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        with open(self.fpath, newline='', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line_no, line in enumerate(csv_reader, 1):
                if line_no < 4:
                    continue
                if self.name_col >= len(line):
                    break
                name = line[self.name_col]

                weight = line[self.weight_col]
                weight = atof(weight.replace("%", "").replace("\xa0", ""))
                ticker = line[self.ticker_col]
                region = line[self.region_col]
                region = EtfReader.get_region_code(LocationCodes.DE_FULL_NAME, region)
                a = Value(name, weight, weight, ticker, region)

                self.update_region(region, weight)
                self.asset.values.append(a)
