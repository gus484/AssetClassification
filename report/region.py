import logging
import json
import os.path
import pprint
from dataclasses import dataclass

log = logging.getLogger("__main__")


class RegionMapping:
    mapping = None

    @staticmethod
    def get_name(short):
        if RegionMapping.mapping is None:
            RegionMapping.load_mapping()

        return RegionMapping.mapping.get(short, 'Welt')

    @staticmethod
    def load_mapping():
        with open("mappings/de_region_names.json", 'r', encoding="utf-8") as f:
            RegionMapping.mapping = json.load(f)


class Gpo:
    mapping = None
    mapping_file_path = "mappings/gpo_mapping3.json"

    @staticmethod
    def set_path_to_mapping_file(path):
        if os.path.exists(path):
            Gpo.mapping_file_path = path

    @staticmethod
    def get_region(short):
        if Gpo.mapping is None:
            Gpo.load_mapping()

        for name, region_shorts in Gpo.mapping.items():
            if short in region_shorts:
                return name
        return 'Welt'

    @staticmethod
    def get_mapping(short):
        if Gpo.mapping is None:
            Gpo.load_mapping()
            Gpo.mapping = Gpo.init_mapping(Gpo.mapping)

        return Gpo.mapping.get(short, ["Welt", short])

    @staticmethod
    def init_mapping(mapping):
        m = {}
        for key, value in mapping.items():

            if type(value) is list:
                for e in value:
                    m[e] = [key, RegionMapping.get_name(e)]
            else:
                mr = Gpo.init_mapping(mapping[key])
                for k, v in mr.items():
                    mr[k].insert(0, key)
                m.update(mr)
        return m

    @staticmethod
    def load_mapping():
        if not os.path.exists(Gpo.mapping_file_path) or not os.path.isfile(Gpo.mapping_file_path):
            log.error("the region mapping file not exist")

        with open(Gpo.mapping_file_path, 'r', encoding="utf-8") as f:
            Gpo.mapping = json.load(f)
        log.debug(f"read region mapping from file: '{Gpo.mapping_file_path}'")


@dataclass
class Region:
    short: str
    weight: float
    num_of_countries: int = 0


if __name__ == "__main__":
    Gpo.load_mapping()
    m = Gpo.init_mapping(Gpo.mapping)
    pprint.pprint(m)
