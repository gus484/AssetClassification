from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class VanguardEtfReader(EtfReader):
    CONFIGS = {}

    def __init__(self, fpath: str, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.VANGUARD

    def read_asset(self):
        self.init_from_config()
        self.open_file()

        name = self.get_name()

        date_obj = self.get_date()
        last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, name)
        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.get_row_count()):

            name = self.get_data(i, self.holding_name_col)
            if name is None:
                break

            weight = self.get_data(i, self.weight_col)
            weight = self.convert_str_to_float(weight)
            ticker = self.get_data(i, self.ticker_col)
            region = self.get_data(i, self.region_col)
            region = EtfReader.get_region_code(LocationCodes[self.location_code], region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)
            self.asset.values.append(a)
