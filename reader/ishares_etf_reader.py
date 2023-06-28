import csv
import os
from datetime import datetime
from locale import atof

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily


class ISharesEtfReader(EtfReader):
    def __init__(self, fpath, sheet=None):
        super().__init__(sheet)
        self.fund_family = FundFamily.ISHARES.value
        self.last_update = ''
        self.header_name = 'Wertpapiere'
        self.header_weight = '% der Assets'
        self.start_row = 4
        self.ticker_col = 0
        self.name_col = 1
        self.weight_col = 5
        self.region_col = 9
        self.fpath = fpath

    def read_asset(self):
        self.name = os.path.basename(os.path.normpath(self.fpath))
        with open(self.fpath, newline='', encoding="utf8") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:
                    self.last_update = line[1]
                    break
        date_format = '%d.%B.%Y'
        date_obj = datetime.strptime(self.last_update, date_format)
        self.last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, self.name)
        self.name = EtfReader.get_name_from_isin(self.fund_family, self.isin)
        self.asset = Asset(self.name, self.isin, 0.0, self.last_update, [])

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
                region = EtfReader.get_region_code(self.fund_family, region)
                a = Value(name, weight, weight, ticker, region)

                self.update_region(region, weight)

                self.asset.values.append(a)
