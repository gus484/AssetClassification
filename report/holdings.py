from report.region import RegionMapping
from report.report import Report
from report.translation import Translation


class HoldingsReport(Report):

    def __init__(self, assets, toc=False):
        super().__init__(self.HTML_HOLDINGS, assets, toc=toc)

    def create(self, holdings):

        rows = []
        for h in holdings:
            rows.append([h])
        rows.sort()

        rows = self.format_data(holdings)

        self.doc.write_infobox([(Translation.get_name("count"), str(len(rows)))])
        self.doc.write_table("Holdings", ['Name', Translation.get_name("country")], rows)

        self.write_file(self.HTML_HOLDINGS)

    def format_data(self, holdings):
        names = list(holdings.keys())
        names.sort()

        data = []
        for name in names:
            data.append([name, RegionMapping.get_name(holdings[name].region)])
        return data
