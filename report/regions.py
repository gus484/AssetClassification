from decimal import *

from report import region
from report.report import Report


class RegionReport(Report):

    def __init__(self, assets, toc):
        super().__init__(self.HTML_REGIONS, assets, ['js/chart.umd.min.js',
                                                     'js/table.js'], toc)

    def create(self):
        getcontext().prec = 4
        self.doc.write_script_tag('js/charts.js')

        for isin, asset in self.assets.items():
            gpo = {}
            regions_tbl_gpo = {}
            regions = asset.get_regions_sorted()

            for short, asset_region in regions.items():
                gpo_region = short

                if gpo_region not in regions_tbl_gpo:
                    regions_tbl_gpo[gpo_region] = [gpo_region, Decimal(asset_region.weight),
                                                   asset_region.num_of_countries]
                else:
                    regions_tbl_gpo[gpo_region][1] += Decimal(asset_region.weight)
                    regions_tbl_gpo[gpo_region][2] += asset_region.num_of_countries
                gpo = self.add_to_gpo_dict(gpo, asset_region)

            regions_chart_gpo = []

            for gpo_region, values in gpo.items():
                regions_chart_gpo.append('%.2f' % values[0][1])

            canvas_id = f"gpo_regions_{isin}"
            self.doc.write_div(f'<canvas id="{canvas_id}"></canvas>', 'chart_box', isin)
            self.doc.write_div('', tag_id=f"div_tbl_{isin}")

            gpo = self.convert_gpo_decimal_to_str(gpo)

            self.doc.write_run_script_after_doc_loaded('print_doughnut_chart',
                                                       canvas_id,
                                                       str([f'{asset.name} ({isin})']),
                                                       str(list(gpo.keys())),
                                                       str(regions_chart_gpo))

            self.doc.write_run_script_after_doc_loaded('createTbl', f"'gpo_tbl_{isin}'",
                                                       str(['Region', 'Weight in %', 'Anz. Holdings']),
                                                       str(gpo),
                                                       f"'div_tbl_{isin}'")

        self.write_file(self.HTML_REGIONS)

    def add_to_gpo_dict(self, gpo, asset_region):
        lmapping = region.Gpo.get_mapping(asset_region.short)

        top_lvl = lmapping[0]
        if top_lvl == 'Welt':
            pass
            # print(asset_region)

        if top_lvl not in gpo:
            gpo[top_lvl] = [[top_lvl, Decimal(asset_region.weight), asset_region.num_of_countries], [[
                lmapping[-1], Decimal(asset_region.weight), asset_region.num_of_countries
            ]]]
        else:
            gpo_val = gpo.get(top_lvl)
            gpo_val[0][1] += Decimal(asset_region.weight)
            gpo_val[0][2] += asset_region.num_of_countries
            gpo_val[1].append([lmapping[-1], Decimal(asset_region.weight), asset_region.num_of_countries])

        return gpo

    def convert_gpo_decimal_to_str(self, gpo):
        for top_lvl, r in gpo.items():
            r[0][1] = '%.2f' % r[0][1]
            for e in r[1]:
                e[1] = '%.2f' % e[1]
        return gpo
