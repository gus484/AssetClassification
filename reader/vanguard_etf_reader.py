from locale import atof

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class VanguardEtfReader(EtfReader):
    REGEX = r'(Vanguard)([\D\s\(\)\-]+)(\s\-\s)*(\d{1,2}.\d{1,2}.\d{2,4})\.(xlsx)'
    DATE_FORMATS = [
        '%d. %B %Y',
        '%d. %b. %Y'
    ]

    def __init__(self, fpath: str):
        super().__init__(fpath)
        self.fund_family = FundFamily.VANGUARD.value
        self.start_row = 8
        self.ticker_col = 1
        self.name_col = 2
        self.weight_col = 3
        self.region_col = 5
        self.read_sheet_from_wb()

    def read_asset(self):
        name = self.sheet.cell(4, 1).value
        last_update = self.sheet.cell(5, 1).value[4:]

        date_obj = self.parse_date(last_update)
        last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, name)
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
            region = EtfReader.get_region_code(LocationCodes.ALPHA_2_CODE, region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
