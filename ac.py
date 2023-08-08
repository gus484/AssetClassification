import argparse
import locale
import logging
import logging.handlers
import os.path
import pathlib
import queue

import report.region
from holdings import Holdings
from reader.etf_reader_factory import EtfReaderFactory
from report.about import AboutReport
from report.region import Gpo
from report.report import Report
from report.report_factory import ReportFactory
from report.translation import Translation

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
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

    def __init__(self, log_queue: queue = None):
        self.cash_filter = []
        self.path_to_cash_filter = "cash_filter.txt"
        self.assets = {}
        self.holdings = None
        self.overlaps = None

        self.idirectory = None
        self.isin_filter = []
        self.version = '0.01'
        self.language = 'de'

        setup_logger(log_queue)

    def read_assets(self):
        if self.idirectory is None or not os.path.exists(self.idirectory):
            log.error('input directory not exists %s', self.idirectory)
            return
        self.assets = EtfReaderFactory.read_etfs_from_path(self.idirectory, self.isin_filter)
        return self.assets

    def merge_holdings(self):
        positions = Holdings.merge_holdings(self.assets)
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

        rep = AboutReport()
        rep.create(self.version)

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-id", "--idirectory", help="input directory")
        arg_parser.add_argument("-od", "--odirectory", help="output path for html report")
        arg_parser.add_argument("-is", "--isin", nargs='+', help="list of interested ISINs")
        arg_parser.add_argument("-gpo", "--gpo_desc", help="path to region mapping json file")
        arg_parser.add_argument("-l", "--language", help="language")
        args = arg_parser.parse_args()

        if args.gpo_desc is not None:
            report.region.Gpo.set_path_to_mapping_file(args.gpo_desc)

        src_path = pathlib.Path().resolve()
        if args.odirectory is not None:
            Report.set_paths(src_path, args.odirectory)

        self.idirectory = args.idirectory

        if args.isin is not None:
            self.isin_filter = args.isin

        if args.language is not None and args.language in ['de', 'en']:
            self.language = args.language

        Translation.set_language(self.language)
        report.region.RegionMapping.set_path_to_mapping_file(self.language)

    def set_parameters(self, idirectory, odirectory, isin_filter, region_mapping, lang):
        self.idirectory = idirectory
        src_path = pathlib.Path().resolve()
        Report.set_paths(src_path, odirectory)
        self.isin_filter = isin_filter
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
        self.read_assets()
        self.merge_holdings()
        self.report()


if __name__ == '__main__':
    app = AssetAllocation()
    app.parse_args()
    app.run()
