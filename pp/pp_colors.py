class PPColor:
    colors = [
        ('#003f5c', ['#1A526C', '#33657D', '#4D798D', '#668C9D', '#809FAE', '#99B2BE']),
        # ('#445D89',	'#596F96',	'#6D81A3',	'#8293B0',	'#97A5BE',	'#ACB7CB']),
        ('#665191', ['#75629C', '#8574A7', '#9485B2', '#A397BD', '#B3A8C8', '#C2B9D3']),
        ('#a05195', ['#AA62A0', '#B374AA', '#BD85B5', '#C697BF', '#D0A8CA', '#D9B9D5']),
        ('#d45087', ['#D86293', '#DD739F', '#E185AB', '#E596B7', '#EAA8C3', '#EEB9CF']),
        ('#f95d6a', ['#FA6D79', '#FA7D88', '#FB8E97', '#FB9EA6', '#FCAEB5', '#FDBEC3']),
        ('#ff7c43', ['#FF8956', '#FF9669', '#FFA37B', '#FFB08E', '#FFBEA1', '#FFCBB4']),
        ('#ffa600', ['#FFAF1A', '#FFB833', '#FFC14D', '#FFCA66', '#FFD380', '#FFDB99']),
    ]

    def __init__(self):
        self.nbr_top_colors = len(PPColor.colors)
        self.nbr_sub_colors = len(PPColor.colors[0][1])

    def get_color(self, lvl: int, idx: int) -> str:
        c_lvl = lvl % self.nbr_top_colors
        if lvl == 0:
            return self.get_top_color(idx)
        else:
            return self.get_sub_color(c_lvl, idx)

    def get_top_color(self, idx: int) -> str:
        color_idx = idx % self.nbr_top_colors
        return PPColor.colors[color_idx][0]

    def get_sub_color(self, top_idx: int, idx: int) -> str:
        color_idx = idx % self.nbr_sub_colors
        print(str(color_idx) + "::" + str(top_idx))
        return PPColor.colors[top_idx][1][color_idx]
