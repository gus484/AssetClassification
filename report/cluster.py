from dataclasses import dataclass, fields, field

from holdings import Overlap
from reader.asset import Asset
from report.report import Report
from report.translation import Translation as T


@dataclass
class ClusterData:
    isin: str
    weight: str = ""
    nbr_of_cluster_positions: int = 0
    nbr_of_holdings: int = 0
    nbr_of_etf_clusters: int = 0
    last_update: str = ""
    cluster_etf_holdings: dict = field(default_factory=dict)

    def get_ibox_data(self):
        """

        :return: A list of tuples that contains the data name and data value
        """
        # return [(T.get_name(field.name), getattr(self, field.name)) for field in fields(self)]
        return [(T.get_name(fields(self)[i].name), getattr(self, fields(self)[i].name)) for i in
                range(len(fields(self)) - 1)]


class ClusterReport(Report):

    def __init__(self, assets, toc=False):
        super().__init__(self.HTML_CLUSTER, assets, ['js/chart.umd.min.js'], toc)

    def create(self, assets, overlaps):
        cds = []
        self.doc.write_script_tag('js/charts.js')
        self.doc.write_script_tag('js/basics.js')
        data = self.create_cluster_tbl_data(assets, overlaps)

        self.doc.write_div(f'<canvas id="chart_overview"></canvas>', 'chart_box')

        for isin, holdings in overlaps.items():
            cd = self.calc_cluster(isin, holdings, assets)
            self.create_etf_info_box(cd)
            self.create_etf_bar_chart(cd, assets)
            self.doc.write_button("Show holdings", f"showElement('tbl_{isin}')")
            self.create_table(data[isin], isin)
            cds.append(cd)

        self.create_overview_bar_chart(cds)
        self.write_file(self.HTML_CLUSTER)

    def calc_cluster(self, isin, holdings, assets):
        c = ClusterData(isin, "", len(holdings), assets[isin].get_num_values(), 0, "")
        c.nbr_of_cluster_positions = len(holdings)
        c.weight = assets[isin].weight
        c.nbr_of_holdings = assets[isin].get_num_values()
        c.last_update = assets[isin].last_history_date

        # iterates over all holdings with cluster risk for ETF with isin
        for holding, data in holdings.items():
            for cluster_isin in data:
                # don't count yourself among the ETFs with overlap.
                if cluster_isin == isin:
                    continue

                cnt = c.cluster_etf_holdings.get(cluster_isin, 0) + 1
                c.cluster_etf_holdings[cluster_isin] = cnt

        c.nbr_of_etf_clusters = len(c.cluster_etf_holdings)
        return c

    def create_etf_info_box(self, cd):
        self.doc.write_infobox(cd.get_ibox_data(), cd.isin)

    def create_table(self, data, isin: str):
        self.doc.write_table(data[0], data[1], data[2], tbl_id=f"tbl_{isin}", tbl_style="display:none;")

    def create_etf_bar_chart(self, cd, assets):
        self.doc.write_div(f'<canvas id="chart_{cd.isin}"></canvas>', 'chart_box')
        etfs = list(cd.cluster_etf_holdings.keys())
        etfs.insert(0, cd.isin)
        counts = list(cd.cluster_etf_holdings.values())
        counts.insert(0, cd.nbr_of_holdings)
        self.doc.write_run_script_after_doc_loaded('printBarChart',
                                                   f"chart_{cd.isin}",
                                                   f'"{assets[cd.isin].name} ({cd.isin})"',
                                                   str(etfs),
                                                   str(counts))

    def create_overview_bar_chart(self, cds):
        axis_labels = []
        labels = ['Positionen', 'Cluster']
        counts = [[], []]
        for cd in cds:
            axis_labels.append(cd.isin)
            counts[0].append(cd.nbr_of_holdings - cd.nbr_of_cluster_positions)
            counts[1].append(cd.nbr_of_cluster_positions)

        self.doc.write_run_script_after_doc_loaded('printStackedBarChart',
                                                   f"chart_overview",
                                                   f'"Übersicht"',
                                                   str(axis_labels),
                                                   str(labels),
                                                   str(counts))

    def create_cluster_tbl_data(self, assets: dict[str, Asset], overlaps: dict[str, Overlap]):
        data = {}

        for curr_etf_isin in overlaps:
            rows = []
            tbl_head = f"{assets[curr_etf_isin].name} ({curr_etf_isin})"
            etf_holdings = sorted(overlaps[curr_etf_isin].keys())

            for holding in etf_holdings:
                holding_rows = self.create_holding_cluster(holding, overlaps[curr_etf_isin][holding])
                rows.extend(holding_rows)

            data[curr_etf_isin] = [tbl_head,
                                   [T.get_name('company'), T.get_name('isin'), T.get_name('weight')],
                                   rows]
        return data

    def create_holding_cluster(self, holding: str, related_etfs):
        row_head = [holding, '', 0.0]
        rows = []

        for isin in related_etfs:
            row_head[2] += related_etfs[isin][0]
            rows.append(['', isin,
                         f"{related_etfs[isin][0]:.2f}"])
        row_head[2] = f"{row_head[2]:.2f}"

        return [row_head] + rows
