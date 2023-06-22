from dataclasses import dataclass, fields, field
from report.translation import Translation as T

from report.report import Report


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
        # data = self.create_cluster_data(assets, overlaps)

        self.doc.write_div(f'<canvas id="chart_overview"></canvas>', 'chart_box')

        for isin, holdings in overlaps.items():
            cd = self.calc_cluster(isin, holdings, assets)
            self.create_etf_info_box(cd)
            self.create_etf_bar_chart(cd, assets)
            cds.append(cd)

        self.create_overview_bar_chart(cds)
        # self.create_table(data)

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

    def create_table(self, data):
        for d in data:
            self.doc.write_infobox(d[0][0], d[0][1])
            self.doc.write_table(d[1][0], d[1][1], d[1][2])

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

    def create_cluster_data(self, assets, overlaps):
        data = []

        for isin in overlaps:
            d = []
            tbl_head = f"{assets[isin].name} ({isin})"
            row = []
            cluster_risk_per = len(overlaps[isin]) * 100.0 / assets[isin].get_num_values()
            cluster_risk = f"{len(overlaps[isin])} / {assets[isin].get_num_values()} ({cluster_risk_per:.2f}%)"

            for holding in sorted(overlaps[isin].keys()):
                row.append([holding, isin,
                            f"{overlaps[isin][holding][isin][0]:.2f}",
                            f"{overlaps[isin][holding][isin][1]:.2f}"])

                for ov_isin in overlaps[isin][holding]:
                    if ov_isin == isin:
                        continue
                    row.append(["",
                                ov_isin,
                                f"{overlaps[isin][holding][ov_isin][0]:.2f}",
                                f"{overlaps[isin][holding][ov_isin][1]:.2f}"])

            ol_etfs = self.count_overlapping_etfs(isin, overlaps)
            d.append([[("Name", assets[isin].name),
                       ("ISIN", isin),
                       ("Gewichtung", assets[isin].weight),
                       ("Klumpen", cluster_risk),
                       ("Klumpen ETF", ol_etfs),
                       ("Datum", assets[isin].last_history_date)],
                      isin])
            d.append([tbl_head, ['Holding', 'ETF', 'Weight', 'Total Weight'], row])
            data.append(d)
        return data

    def count_overlapping_etfs(self, isin, overlaps):
        ol_etfs = {}
        for v in overlaps[isin].values():
            for vd in v:
                if vd not in ol_etfs and vd != isin:
                    ol_etfs[vd] = 0
                elif vd != isin:
                    ol_etfs[vd] += 1
        # print(ol_etfs)
        return len(ol_etfs)
