import glob
import logging
import re
from pathlib import Path

from reader.etf_reader import FundFamily, EtfReader
from reader.ishares_etf_reader import ISharesEtfReader
from reader.spdr_etf_reader import SpdrEtfReader
from reader.vaneck_etf_reader import VanEckEtfReader
from reader.vanguard_etf_reader import VanguardEtfReader

log = logging.getLogger("ac")


class EtfReaderFactory:
    READERS = {
        FundFamily.ISHARES: (ISharesEtfReader.REGEX, ISharesEtfReader),
        FundFamily.SPDR: (SpdrEtfReader.REGEX, SpdrEtfReader),
        FundFamily.VANECK: (VanEckEtfReader.REGEX, VanEckEtfReader),
        FundFamily.VANGUARD: (VanguardEtfReader.REGEX, VanguardEtfReader)
    }

    @staticmethod
    def get_reader(fpath):
        reader = None
        file_name = Path(fpath).name

        for k, v in EtfReaderFactory.READERS.items():
            if re.search(v[0], file_name) is not None:
                log.debug(f"{k} => {file_name}")
                reader = v[1](fpath)
                break
        return reader

    @staticmethod
    def read_etfs_from_path(path, isin_filter):
        etfs = {}
        file_list = glob.glob(path + '/*')
        for file in file_list:
            try:
                etf = EtfReaderFactory.read_etf_from_file(file, isin_filter)
                if etf is not None:
                    etfs[etf.isin] = etf
            except Exception as e:
                log.warning(f"Could not read file:{file}", e)

        return etfs

    @staticmethod
    def read_etf_from_file(fpath: str, isin_filter: list[str]):
        r = EtfReaderFactory.get_reader(fpath)

        if r is None:
            return None

        r.read_asset()

        if r.isin == EtfReader.NOT_EXIST:
            log.warning(f"Could not get ISIN for {r.fpath}")
            return None

        if r.isin not in isin_filter and len(isin_filter) > 0:
            return None

        r.read_sheet()
        return r.asset
