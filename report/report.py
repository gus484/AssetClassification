import logging
import os.path
import shutil

from report.html import Html
from report.translation import Translation as T

log = logging.getLogger("ac")


class Report:
    HTML_CLUSTER = 'Cluster'
    HTML_HOLDINGS = 'Holdings'
    HTML_REGIONS = 'Regions'
    HTML_ABOUT = 'About'
    HTML_FILES = {
        HTML_CLUSTER: 'cluster.html',
        HTML_HOLDINGS: 'holdings.html',
        HTML_REGIONS: 'regions.html',
        HTML_ABOUT: 'about.html'
    }

    REPORT_SRC_PATH = ""
    REPORT_PATH = ""

    def __init__(self, title, assets, scripts=None, toc=False):
        self.assets = assets
        self.page = title
        self.doc = Html(title, scripts)
        self.create_main_menu()
        if toc:
            toc = self.create_toc_from_assets()
            self.doc.write_toc(toc)

    def create_main_menu(self):
        self.doc.write_link_bar([(T.get_name('companys'), 'holdings.html'),
                                 (T.get_name('cluster_risk'), 'cluster.html'),
                                 (T.get_name('regions'), 'regions.html')], self.page)

    def create_toc_from_assets(self):
        toc = []
        for a in self.assets:
            toc.append((self.assets[a].name, a))
        return toc

    def write_about_link(self):
        data = f'<a href="about.html">{T.get_name("about")}</a>'
        self.doc.write_div(data, 'about')

    def write_file(self, report_type):
        self.write_about_link()

        file_name = self.HTML_FILES[report_type]
        file_path = os.path.join(self.REPORT_PATH, file_name)

        self.doc.write_to_file(file_path)

    @staticmethod
    def set_paths(src_path, dest_path):
        Report.REPORT_SRC_PATH = src_path

        if os.path.exists(dest_path) and os.path.isdir(dest_path):
            log.debug("set report directory to: %s", [dest_path])
            Report.REPORT_PATH = dest_path
            try:
                Report.__copy_static_files()
            except FileNotFoundError:
                log.error("report assets not found")

    @staticmethod
    def __copy_static_files():
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "js"),
                        os.path.join(Report.REPORT_PATH, "js"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "img"),
                        os.path.join(Report.REPORT_PATH, "img"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "css"),
                        os.path.join(Report.REPORT_PATH, "css"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "license"),
                        os.path.join(Report.REPORT_PATH, "license"), dirs_exist_ok=True)
