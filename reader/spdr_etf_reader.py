from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class SpdrEtfReader(EtfReader):
    def __init__(self, fpath: str, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.SPDR

    def read_asset(self):
        self.init_from_config()
        self.open_file()

        name = self.get_name()
        self.isin = self.get_isin()

        date_obj = self.get_date()
        last_update = date_obj.strftime('%d.%m.%Y')

        self.asset = Asset(name, self.isin, 0.0, last_update, [])

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
