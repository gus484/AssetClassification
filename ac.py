import argparse
import locale
import logging
import logging.handlers
import os.path
import pathlib
import queue

import report.region
from holdings import Holdings
from pp.pp_updater import PPUpdater
from reader.etf_reader_factory import EtfReaderFactory
from report.about import AboutReport
from report.region import Gpo
from report.report import Report
from report.report_factory import ReportFactory
from report.translation import Translation

try:
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
except locale.Error as e:
    print("Could not load local 'de_DE.utf8'")
log = logging.getLogger("ac")


class QueueFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return f"{record.levelname}: {message}"


def setup_logger(log_queue):
    log.setLevel(logging.DEBUG)

    file = logging.FileHandler("asset.log", encoding="UTF-8")
    file.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", datefmt="%d.%m.%y - %H:%M:%S")
    file.setFormatter(file_format)

    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    stream_format = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s", datefmt="%d.%m.%y - %H:%M:%S")
    stream.setFormatter(stream_format)

    if log_queue is not None:
        queue_handler = logging.handlers.QueueHandler(log_queue)
        queue_handler.setLevel(logging.INFO)
        queue_formatter = QueueFormatter(fmt="%(message)s")
        queue_handler.setFormatter(queue_formatter)
        log.addHandler(queue_handler)

    log.addHandler(stream)
    log.addHandler(file)


class AssetAllocation:
    VERSION = '0.2'

    def __init__(self, log_queue: queue = None):
        self.cash_filter = []
        self.path_to_cash_filter = "cash_filter.txt"
        self.assets = {}
        self.holdings = None
        self.overlaps = None

        self.idirectory = None
        self.isin_filter = []
        self.language = 'de'
        self.pp_file = None
        self.pp_data = {}

        setup_logger(log_queue)

    def read_assets(self):
        if self.idirectory is None or not os.path.exists(self.idirectory):
            log.error('input directory not exists %s', self.idirectory)
            return
        self.assets = EtfReaderFactory.read_etfs_from_path(self.idirectory, self.isin_filter)
        return self.assets

    def merge_holdings(self):
        positions = Holdings.merge_holdings(self.assets)
        positions = Holdings.remove_cash_positions(positions, self.cash_filter)
        duplicates = Holdings.find_duplicates(list(positions.keys()))
        self.holdings = Holdings.remove_duplicates(positions, duplicates)
        self.overlaps = Holdings.create_overlaps(self.holdings)

    def report(self):
        # report_holdings
        rep = ReportFactory.get_reporter(Report.HTML_HOLDINGS, assets=[])
        rep.create(self.holdings)

        # report_cluster
        rep = ReportFactory.get_reporter(Report.HTML_CLUSTER, self.assets)
        rep.create(self.assets, self.overlaps)

        # report_regions
        rep = ReportFactory.get_reporter(Report.HTML_REGIONS, self.assets)
        rep.create()
        self.pp_data = rep.get_gpo_data()

        rep = AboutReport()
        rep.create(AssetAllocation.VERSION)

    def parse_args(self) -> int:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-src", "--src_path", help="source path")
        arg_parser.add_argument("-target", "--target_path", help="target path for html report")
        arg_parser.add_argument("-is", "--isin", nargs='+', help="list of interested ISINs")
        arg_parser.add_argument("-region", "--region_mapping", help="path to region mapping json file")
        arg_parser.add_argument("-l", "--language", help="language")
        args = arg_parser.parse_args()

        if args.region_mapping is not None:
            report.region.Gpo.set_path_to_mapping_file(args.region_mapping)

        src_path = pathlib.Path().resolve()

        if args.src_path is None or not os.path.isdir(args.src_path):
            log.error("No source or not existing path defined!")
            return False

        if args.target_path is None or not os.path.isdir(args.target_path):
            log.error("No target or not existing path defined!")
            return False

        Report.set_paths(src_path, args.target_path)
        self.idirectory = args.src_path

        if args.isin is not None:
            self.isin_filter = args.isin

        if args.language is not None and args.language in ['de', 'en']:
            self.language = args.language

        Translation.set_language(self.language)
        report.region.RegionMapping.set_path_to_mapping_file(self.language)

        return True

    def set_parameters(self, idirectory, odirectory, isin_filter, region_mapping, lang, pp_file):
        self.idirectory = idirectory
        src_path = pathlib.Path().resolve()
        Report.set_paths(src_path, odirectory)
        self.isin_filter = isin_filter
        self.pp_file = pp_file
        Gpo.set_path_to_mapping_file(region_mapping)
        self.language = lang
        Translation.set_language(lang)
        report.region.RegionMapping.set_path_to_mapping_file(lang)

    def read_cash_filter(self):
        if not os.path.exists(self.path_to_cash_filter) or not os.path.isfile(self.path_to_cash_filter):
            log.error("the cash filter file not exist")

        with open(self.path_to_cash_filter, "r") as reader:
            for line in reader:
                self.cash_filter.append(line.strip())
        log.debug(f"read cash filter from file: '{self.path_to_cash_filter}'")

    def run(self):
        self.read_cash_filter()
        log.info("Stage 1: read files")
        self.read_assets()
        log.info("Stage 2: merge holdings")
        self.merge_holdings()
        log.info("Stage 3: create report")
        self.report()
        if self.pp_file:
            log.info("Stage 4: write to pp file")
            pp = PPUpdater(self.pp_file, '')
            pp.run(self.pp_data)
        log.info("finished")


if __name__ == '__main__':
    app = AssetAllocation()
    if not app.parse_args():
        exit(0)
    app.run()
