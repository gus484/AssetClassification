from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class SpdrEtfReader(EtfReader):
    def __init__(self, fpath: str, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.SPDR

    def read_asset(self):
        super().read_asset()

        name = self.get_name()
        self.isin = self.get_isin()

        date_obj = self.get_date()

        self.asset = Asset(name, self.isin, 0.0, date_obj, [])

    def read_sheet(self):
        for i in range(self.start_row, self.sheet.max_row):
            name = self.get_data(i, self.holding_name_col)
            if name is None:
                break
            weight = self.get_data(i, self.weight_col)
            if weight == '-':
                continue
            ticker = self.get_data(i, self.ticker_col)
            region = self.get_data(i, self.region_col)
            region = EtfReader.get_region_code(LocationCodes[self.location_code], region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
