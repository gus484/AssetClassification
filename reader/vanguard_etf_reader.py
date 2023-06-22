from datetime import datetime
from locale import atof

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader


class VanguardEtfReader(EtfReader):
    def __init__(self, sheet):
        super().__init__(sheet)
        self.fund_family = 'VANGUARD'
        self.last_update = ''
        self.header_name = 'Wertpapiere'
        self.header_weight = '% der Assets'
        self.start_row = 8
        self.ticker_col = 1
        self.name_col = 2
        self.weight_col = 3
        self.region_col = 5
        self.sheet = sheet

    def read_asset(self):
        self.name = self.sheet.cell(4, 1).value
        self.last_update = self.sheet.cell(5, 1).value[4:]

        date_format = '%d. %B %Y'
        date_obj = datetime.strptime(self.last_update, date_format)
        self.last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, self.name)
        self.asset = Asset(self.name, self.isin, 0.0, self.last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.sheet.max_row):
            name = self.sheet.cell(i, self.name_col).value
            if name is None:
                break
            weight = self.sheet.cell(i, self.weight_col).value
            weight = atof(weight.replace("%", "").replace("\xa0", ""))
            ticker = self.sheet.cell(i, self.ticker_col).value
            region = self.sheet.cell(i, self.region_col).value
            region = EtfReader.get_region_code(self.fund_family, region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
