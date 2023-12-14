from dataclasses import dataclass


@dataclass
class Position:
    name: str
    isin: str
    region: str
    related_etfs: dict


@dataclass()
class Weight:
    weight: float
    weight_total: float


@dataclass
class Overlap:
    isin: str
    weights: Weight


class Holdings:

    @staticmethod
    def merge_holdings(assets):
        positions = {}

        for k, v in assets.items():
            for h in v.values:
                holding = h.name.upper()

                if holding not in positions:
                    positions[holding] = Position(holding, '', h.region, {})

                positions[holding].related_etfs[v.isin] = (h.weight, h.weight_total)

        return positions

    @staticmethod
    def find_duplicates(positions: list[str]) -> list[tuple]:
        # Tries to find out duplicates by checking similar names
        positions.sort()
        duplicates = []

        for i in range(len(positions)):
            if i + 1 > len(positions) - 1:
                break
            nxt_name = positions[i + 1]
            curr_name = positions[i]
            if nxt_name.startswith(curr_name):
                duplicates.append((curr_name, nxt_name))
        return duplicates

    @staticmethod
    def remove_duplicates(positions: dict[str: Position], duplicates) -> list[Position]:
        # Removes the duplicates and merges the data
        pre_holding = ""
        for curr_name, nxt_name in duplicates:
            value = positions[nxt_name].related_etfs

            if curr_name in positions:
                pre_holding = curr_name
                positions[curr_name].related_etfs.update(value)
            else:
                positions[pre_holding].related_etfs.update(value)

            del positions[nxt_name]
        return positions

    @staticmethod
    def remove_cash_positions(positions: list[Position], cash_filter: list[str]):
        for cash_name in cash_filter:
            positions.pop(cash_name, None)
        return positions

    @staticmethod
    def create_overlaps(holdings: dict[str: Position]) -> dict:
        """
        Returns a dict with etf isin as key and a dict as value. The sub dict contains the etf isin as keys and a tuple
        of weights
        :param holdings:
        :return:
        """
        overlaps = {}
        for holding, holding_data in holdings.items():
            if len(holding_data.related_etfs) == 1:
                continue
            for isin in holding_data.related_etfs:
                if isin not in overlaps:
                    overlaps[isin] = {}
                overlaps[isin][holding_data.name] = holding_data.related_etfs
        return overlaps
