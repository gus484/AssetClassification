import os

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes


class VanEckEtfReader(EtfReader):

    def __init__(self, fpath, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.VANECK
        self.file_name = os.path.basename(self.fpath)

    def read_asset(self):
        self.init_from_config()
        self.open_file()

        self.file_name = self.file_name.split("_")[0]

        date_obj = self.get_date()
        last_update = date_obj.strftime('%d.%m.%Y')

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, self.file_name)
        name = EtfReader.get_name_from_isin(self.fund_family, self.isin)
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

            region = region[:2]
            region = EtfReader.get_region_code(LocationCodes[self.location_code], region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)

            self.asset.values.append(a)
