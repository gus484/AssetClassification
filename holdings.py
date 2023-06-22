

class Holdings:

    @staticmethod
    def merge_holdings(assets):
        md = {}
        for k, v in assets.items():
            for h in v.values:
                holding = h.name.upper()

                if holding not in md:
                    md[holding] = {}

                md[holding][v.isin] = (h.weight, h.weight_total)
        return md

    @staticmethod
    def find_duplicates(holdings):
        names = list(holdings.keys())
        names.sort()
        duplicates = []

        for i in range(len(names)):
            if i + 1 > len(names) - 1:
                break
            nxt_name = names[i + 1]
            curr_name = names[i]
            if nxt_name.startswith(curr_name):
                duplicates.append((curr_name, nxt_name))
        return duplicates

    @staticmethod
    def remove_duplicates(holdings, duplicates):
        pre_holding = ""
        for d in duplicates:
            value = holdings[d[1]]
            # (f"{d[0]}::{d[1]}")
            if d[0] in holdings:
                holdings[d[0]].update(value)
                pre_holding = d[0]
            else:
                holdings[pre_holding].update(value)

            del holdings[d[1]]
        return holdings

    @staticmethod
    def create_overlaps(holdings):
        """
        Returns a dict with etf isin as key and a dict as value. The sub dict contains the etf isin as keys and a tuple
        of weights
        :param holdings:
        :return:
        """
        overlaps = {}
        for holding in holdings:
            if len(holdings[holding]) == 1:
                continue
            for a in holdings[holding]:
                if a not in overlaps:
                    overlaps[a] = {}
                overlaps[a][holding] = holdings[holding]
        return overlaps
