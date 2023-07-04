import datetime

from report.region import Gpo
from report.report import Report
from report.translation import Translation


class AboutReport(Report):

    def __init__(self):
        super().__init__(self.HTML_ABOUT, None, [], False)

    def create(self, version):
        self.doc.write_infobox([['Version', version],
                                ['Created', datetime.datetime.now()],
                                ['Mapping', Gpo.mapping_file_path],
                                ['Translation', Translation.path]])

        self.write_libs()

        self.write_file(self.HTML_ABOUT)

    def write_libs(self):
        data = '<ul>'
        data += '<li>Favicon by <a href="https://icons8.de/">Icons8</a></li>'
        data += '<li>Charts by <a href="www.chartjs.org/">Chart.js</a></li>'
        data += '</ul>'
        self.doc.write_div(data, 'container')
