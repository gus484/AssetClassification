import configparser
import glob
import logging
import os
import re
from pathlib import Path

from reader.etf_reader import FundFamily, EtfReader
from reader.etf_reader_configs import EtfReaderConfigs
from reader.ishares_etf_reader import ISharesEtfReader
from reader.lgim_etf_reader import LGIMEtfReader
from reader.spdr_etf_reader import SpdrEtfReader
from reader.vaneck_etf_reader import VanEckEtfReader
from reader.vanguard_etf_reader import VanguardEtfReader
from reader.xtrackers_etf_reader import XtrackersEtfReader

log = logging.getLogger("ac")


class EtfReaderFactory:
    READERS = {
        FundFamily.ISHARES: ISharesEtfReader,
        FundFamily.LGIM: LGIMEtfReader,
        FundFamily.SPDR: SpdrEtfReader,
        FundFamily.VANECK: VanEckEtfReader,
        FundFamily.VANGUARD: VanguardEtfReader,
        FundFamily.XTRACKERS: XtrackersEtfReader
    }

    READERS_CONFIGS = {}

    @staticmethod
    def get_reader(fpath) -> EtfReader:
        reader = None
        file_name = Path(fpath).name

        for fund_family, reader_class in EtfReaderFactory.READERS.items():
            config, config_name = EtfReaderFactory.check_reader(fund_family, file_name)

            if config is not None:
                log.debug(f"{fund_family} => {file_name}")
                reader = reader_class(fpath, config_name)
                break

        if reader is None:
            log.error(f"Could not identify ETF {file_name}")

        return reader

    @staticmethod
    def check_reader(family, file_name):
        readers = EtfReaderConfigs.get_family_configs(family)

        for name, config in readers.items():
            regex = config['BASE']['regex']
            if re.search(regex, file_name) is None:
                continue

            if config['BASE']['sub_detection'] == "False":
                # if no sub detection is necessary  we know at this point the right config name
                return config, name
            return config, None
        return None, None

    @staticmethod
    def read_config(family: FundFamily, config_path):
        if config_path:
            config_path = os.path.join(config_path, "reader", "configs")
        else:
            config_path = os.path.join("reader", "configs")

        search_word = f"{family.value.lower()}.ini"
        file_list = glob.glob(config_path + '/*')
        for file_path in file_list:
            if not file_path.endswith(search_word):
                continue

            config = configparser.ConfigParser()
            config.read(file_path)

            EtfReaderConfigs.add_config(family, os.path.basename(file_path), config)

    @staticmethod
    def init_readers(config_path: str = None):
        if len(EtfReaderFactory.READERS_CONFIGS) > 0:
            return

        for family, reader_class in EtfReaderFactory.READERS.items():
            EtfReaderFactory.read_config(family, config_path)

    @staticmethod
    def read_etfs_from_path(path, isin_filter):
        etfs = {}
        EtfReaderFactory.init_readers()

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

        if r.isin not in isin_filter and len(isin_filter) > 0:
            return None

        r.read_sheet()
        return r.asset
