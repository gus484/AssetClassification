import datetime
from dataclasses import dataclass, field
from typing import Dict

from report import region


@dataclass
class Value:
    name: str
    weight: float
    weight_total: float
    ticker: str = ''
    region: int = 0


@dataclass
class Asset:
    name: str
    isin: str
    weight: float
    last_history_date: datetime.datetime
    values: list[Value]
    regions: Dict[str, region.Region] = field(default_factory=dict)

    def get_num_values(self):
        return len(self.values)

    def get_regions_sorted(self):
        return self.regions
        # return dict(sorted(self.regions.items(), key=lambda x: x[1], reverse=True))
