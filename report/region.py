import json
import logging
import os.path
from dataclasses import dataclass
from json import JSONDecodeError

log = logging.getLogger("ac")


class RegionMapping:
    mapping = None
    mapping_file_path = os.path.join("mappings", "de_region_names.json")

    @staticmethod
    def set_path_to_mapping_file(path):
        path = os.path.join("mappings", f"{path}_region_names.json")
        if os.path.exists(path):
            RegionMapping.mapping_file_path = path

    @staticmethod
    def get_name(short):
        if RegionMapping.mapping is None:
            RegionMapping.load_mapping()

        return RegionMapping.mapping.get(short, 'Welt')

    @staticmethod
    def load_mapping():
        with open(RegionMapping.mapping_file_path, 'r', encoding="utf-8") as f:
            try:
                RegionMapping.mapping = json.load(f)
            except JSONDecodeError:
                log.error(f"Could not read region names: {RegionMapping.mapping_file_path}")
                RegionMapping.mapping = {}


class Gpo:
    mapping = None
    mapping_file_path = os.path.join("mappings", "region", "gpo.json")

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
            Gpo.mapping = {}
            return

        with open(Gpo.mapping_file_path, 'r', encoding="utf-8") as f:
            try:
                Gpo.mapping = json.load(f)
            except JSONDecodeError:
                log.error(f"Could not read region mapping: {Gpo.mapping_file_path}")
                Gpo.mapping = {}
        log.debug(f"read region mapping from file: '{Gpo.mapping_file_path}'")


@dataclass
class Region:
    short: str
    weight: float
    num_of_countries: int = 0
