import logging
import os.path
import shutil

from report.html import Html

log = logging.getLogger("__main__")


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
        self.doc.write_link_bar([('Holdings', 'holdings.html'),
                                 ('Cluster', 'cluster.html'),
                                 ('Regions', 'regions.html')], self.page)

    def create_toc_from_assets(self):
        toc = []
        for a in self.assets:
            toc.append((self.assets[a].name, a))
        return toc

    def write_about_link(self):
        data = '<a href="about.html">About</a>'
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
            log.info("set report directory to: %s", [dest_path])
            Report.REPORT_PATH = dest_path
            Report.__copy_static_files()

    @staticmethod
    def __copy_static_files():
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "js"),
                        os.path.join(Report.REPORT_PATH, "js"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "img"),
                        os.path.join(Report.REPORT_PATH, "img"), dirs_exist_ok=True)
        shutil.copytree(os.path.join(Report.REPORT_SRC_PATH, "html", "css"),
                        os.path.join(Report.REPORT_PATH, "css"), dirs_exist_ok=True)