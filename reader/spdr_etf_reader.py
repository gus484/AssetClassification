from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class SpdrEtfReader(EtfReader):
    REGEX = r'(holdings)([a-z-0-9]*)(.xlsx)'

    def __init__(self, fpath: str):
        super().__init__(fpath)
        self.fund_family = FundFamily.SPDR.value
        self.start_row = 7
        self.ticker_col = 1
        self.name_col = 3
        self.weight_col = 6
        self.region_col = 7
        self.read_sheet_from_wb()

    def read_asset(self):
        name = self.sheet.cell(1, 2).value
        last_update = self.sheet.cell(4, 2).value
        self.isin = self.sheet.cell(2, 2).value

        date_obj = self.parse_date(last_update)
        last_update = date_obj.strftime('%d.%m.%Y')

        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.sheet.max_row):
            name = self.sheet.cell(i, self.name_col).value
            if name is None:
                break
            weight = self.sheet.cell(i, self.weight_col).value
            if weight == '-':
                continue
            ticker = self.sheet.cell(i, self.ticker_col).value
            region = self.sheet.cell(i, self.region_col).value
            region = EtfReader.get_region_code(LocationCodes.EN_FULL_NAME, region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
