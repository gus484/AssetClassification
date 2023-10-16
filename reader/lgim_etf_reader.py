import csv
import locale
import os
from locale import atof

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily


class LGIMEtfReader(EtfReader):
    REGEX = r'(Fund-holding)[A-Za-z0-9\_\-]+\.(csv)'

    def __init__(self, fpath: str):
        super().__init__(fpath)
        self.fund_family = FundFamily.LGIM.value
        self.start_row = 19
        self.ticker_col = 1
        self.name_col = 0
        self.weight_col = 12
        self.region_col = 1

    def read_asset(self):
        name = os.path.basename(os.path.normpath(self.fpath))
        with open(self.fpath, newline='', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 3:
                    name = line[1]

                if line_no == 4:
                    self.isin = line[1]

                if line_no == 5:
                    last_update = line[1]
                    break

        date_obj = self.parse_date(last_update, ['%Y%m%d'])
        last_update = date_obj.strftime('%d.%m.%Y')

        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        loc = locale.getlocale()
        locale.setlocale(locale.LC_ALL, 'en_US')
        with open(self.fpath, newline='', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line_no, line in enumerate(csv_reader, 1):
                if line_no < self.start_row:
                    continue
                name = line[self.name_col]

                if name == '':
                    break

                weight = line[self.weight_col]
                weight = atof(weight) * 100.0
                ticker = line[self.ticker_col]
                region = line[self.region_col][:2]
                region = EtfReader.get_region_code(self.fund_family, region)
                a = Value(name, weight, weight, ticker, region)
                self.update_region(region, weight)
                self.asset.values.append(a)
        locale.setlocale(locale.LC_ALL, loc)  # restore saved locale
