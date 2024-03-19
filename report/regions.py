from decimal import *

from report import region
from report.region import Region
from report.report import Report


class RegionReport(Report):

    def __init__(self, assets, toc):
        super().__init__(self.HTML_REGIONS, assets, ['js/chart.umd.min.js',
                                                     'js/table.js'], toc)
        self.region_mapping_store = {}

    def create(self):
        getcontext().prec = 4
        self.doc.write_script_tag('js/charts.js')

        for isin, asset in self.assets.items():
            asset_region_distribution = self.calc_regional_distribution(asset.get_regions_sorted().values())
            self.print_chart_and_tbl(asset, asset_region_distribution)

        self.write_file(self.HTML_REGIONS)

    def print_chart_and_tbl(self, asset, region_distribution):
        isin = asset.isin
        region_chart = []

        for values in region_distribution.values():
            region_chart.append('%.2f' % values[0][1])

        canvas_id = f"region_distribution_{isin}"
        self.doc.write_div(f'<canvas id="{canvas_id}"></canvas>', 'chart_box', isin)
        self.doc.write_div('', tag_id=f"div_tbl_{isin}")

        region_distribution_stringified = self.convert_decimal_to_str(region_distribution)
        self.region_mapping_store[isin] = region_distribution_stringified

        self.doc.write_run_script_after_doc_loaded('print_doughnut_chart',
                                                   canvas_id,
                                                   str([f'{asset.name} ({isin})']),
                                                   str(list(region_distribution_stringified.keys())),
                                                   str(region_chart))

        self.doc.write_run_script_after_doc_loaded('createTbl', f"'region_distribution_tbl_{isin}'",
                                                   str(['Region', 'Weight in %', 'Anz. Holdings']),
                                                   str(region_distribution_stringified),
                                                   f"'div_tbl_{isin}'")

    def get_region_distribution(self):
        return self.region_mapping_store

    def calc_regional_distribution(self, asset_regions: list[Region]):
        region_data = {}
        for asset_region in asset_regions:
            region_data = self.update_region_data(region_data, asset_region)
        return region_data

    def update_region_data(self, region_distribution, asset_region):
        lmapping = region.Gpo.get_mapping(asset_region.short)

        top_lvl = lmapping[0]
        if top_lvl == 'Welt':
            name = region.RegionMapping.get_name(asset_region.short)
            if name != 'Welt':
                lmapping[1] = name

        if top_lvl not in region_distribution:
            region_distribution[top_lvl] = [[top_lvl, Decimal(asset_region.weight), asset_region.num_of_holdings], [[
                lmapping[-1], Decimal(asset_region.weight), asset_region.num_of_holdings
            ]]]
        else:
            region_data = region_distribution.get(top_lvl)
            region_data[0][1] += Decimal(asset_region.weight)
            region_data[0][2] += asset_region.num_of_holdings
            region_data[1].append([lmapping[-1], Decimal(asset_region.weight), asset_region.num_of_holdings])

        return region_distribution

    def convert_decimal_to_str(self, region_distribution):
        for top_lvl, r in region_distribution.items():
            r[0][1] = '%.2f' % r[0][1]
            for e in r[1]:
                e[1] = '%.2f' % e[1]
        return region_distribution
