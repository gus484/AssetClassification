import logging
import os

from reader.asset import Asset, Value
from reader.etf_reader import EtfReader, FundFamily, LocationCodes

log = logging.getLogger("ac")


class ISharesEtfReader(EtfReader):
    CONFIGS = {}

    def __init__(self, fpath: str, config_name: str = None):
        super().__init__(fpath, config_name)
        self.fund_family = FundFamily.ISHARES

    def read_asset(self):
        self.open_file()
        if not self.find_config():
            return

        self.init_from_config()

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
        if self.name_row:
            name = self.get_data(self.name_row, self.name_col)
        else:
            name = EtfReader.get_name_from_isin(self.fund_family, self.isin)

        self.asset = Asset(name, self.isin, 0.0, last_update, [])

    def read_sheet(self):
        for line_nbr in range(self.start_row, self.get_row_count()):
            line = self.raw_data[line_nbr]

            if self.weight_col >= len(line):
                break

            ticker = line[self.ticker_col]
            name = line[self.holding_name_col]
            weight = self.convert_str_to_float(line[self.weight_col])
            region = line[self.region_col]
            region = EtfReader.get_region_code(LocationCodes[self.location_code], region)
            a = Value(name, weight, weight, ticker, region)

            self.update_region(region, weight)
            self.asset.values.append(a)
