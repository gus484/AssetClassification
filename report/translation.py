import json
import logging
import os.path
from json import JSONDecodeError

log = logging.getLogger("ac")


class Translation:
    mapping = None
    path = None

    @staticmethod
    def get_name(short):
        if Translation.mapping is None:
            Translation.load_translation()

        return Translation.mapping.get(short, short)

    @staticmethod
    def load_translation():
        if Translation.path is None:
            Translation.mapping = {}
            return

        with open(Translation.path, 'r', encoding="utf-8") as f:
            try:
                Translation.mapping = json.load(f)
                log.debug("loaded translation from file: '%s'", Translation.path)
            except JSONDecodeError:
                log.error(f"Could not read language file:{Translation.path}")
                Translation.mapping = {}

    @staticmethod
    def set_language(lang):
        path = os.path.join("mappings", f"{lang}_translation.json")
        if os.path.exists(path) and os.path.isfile(path):
            Translation.path = path
            Translation.load_translation()

        else:
            log.debug("Language file %s not exists!", path)
