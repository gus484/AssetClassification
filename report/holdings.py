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

        self.doc.write_infobox([(Translation.get_name("count"), str(len(rows)))])
        self.doc.write_table("Holdings", ['Name'], rows)

        self.write_file(self.HTML_HOLDINGS)
