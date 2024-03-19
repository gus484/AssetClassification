import logging
import os

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes

log = logging.getLogger("ac")


class ISharesEtfReader(EtfReader):

    def __init__(self, fpath: str, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.ISHARES

    def read_asset(self):
        super().read_asset()

        file_name = os.path.basename(os.path.normpath(self.fpath))
        date_obj = self.get_date()
        last_update = date_obj.strftime('%d.%m.%Y')

        '''      
                if line_no == 3:
                    # normally there are 12 cols
                    if len(line) == 13:
                        self.weight_col += 1
                        self.region_col += 1
                    break'''

        self.isin = EtfReader.get_isin_from_file_name(self.fund_family, file_name)
        name = self.get_name()

        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for i in range(self.start_row, self.get_row_count()):
            name = self.get_data(i, self.holding_name_col)

            if name is None:
                break

            ticker = self.get_data(i, self.ticker_col)
            weight = self.convert_str_to_float(self.get_data(i, self.weight_col))
            region = self.get_data(i, self.region_col)
            region = EtfReader.get_region_code(LocationCodes[self.location_code], region)

            a = Value(name, weight, weight, ticker, region)
            self.asset.values.append(a)
            self.update_region(region, weight)
