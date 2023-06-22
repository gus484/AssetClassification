import abc

from report.cluster import ClusterReport
from report.holdings import HoldingsReport
from report.regions import RegionReport
from report.report import Report


class ReportFactory:

    @staticmethod
    def get_reporter(rtype, assets):
        if rtype == Report.HTML_HOLDINGS:
            return HoldingsReport(assets)
        if rtype == Report.HTML_CLUSTER:
            return ClusterReport(assets, True)
        if rtype == Report.HTML_REGIONS:
            return RegionReport(assets, True)
        return None

    @abc.abstractmethod
    def create(self):
        """Method documentation"""
        return
