import os

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class XtrackersEtfReader(EtfReader):

    def __init__(self, fpath: str, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.XTRACKERS

    def read_asset(self):
        self.open_file()
        self.init_from_config()

        name = os.path.basename(self.fpath)
        last_update = self.get_date()
        last_update = last_update.strftime('%d.%m.%Y')

        self.isin = self.get_isin()
        self.isin = self.isin.split("_")[1]

        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.get_row_count()):
            name = self.get_data(i, self.holding_name_col)
            if name is None:
                break
            weight = self.get_data(i, self.weight_col)

            if not type(weight) is float:
                continue

            ticker = self.get_data(i, self.ticker_col)
            region = self.get_data(i, self.region_col)
            region = EtfReader.get_region_code(LocationCodes[self.location_code], region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)
            self.asset.values.append(a)
