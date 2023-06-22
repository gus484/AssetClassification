import glob
import os

from openpyxl.reader.excel import load_workbook

from reader.ishares_etf_reader import ISharesEtfReader
from reader.vanguard_etf_reader import VanguardEtfReader


class EtfReaderFactory:

    @staticmethod
    def get_reader(fpath, ext):
        if ext == '*.csv':
            reader = ISharesEtfReader(fpath)
        elif ext == '*.xlsx':
            wb = load_workbook(filename=fpath)
            sheet = wb.active
            reader = VanguardEtfReader(sheet)
        return reader

    @staticmethod
    def read_files_from_path(path, isin_filter):
        assets = {}
        extensions = ('*.xlsx', '*.csv')
        for ext in extensions:
            for f in glob.glob(os.path.join(path, ext)):
                r = EtfReaderFactory.get_reader(f, ext)
                r.read_asset()
                r.read_sheet()
                if r.isin not in isin_filter and len(isin_filter) > 0:
                    continue
                assets[r.isin] = r.asset
        return assets
