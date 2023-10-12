import os

from reader.etf_reader import EtfReader
from reader.etf_reader_factory import EtfReaderFactory


def create_reader(test_file_name) -> EtfReader:
    file = os.path.join(os.path.dirname(__file__), f'data/{test_file_name}')
    reader = EtfReaderFactory.get_reader(file)
    return reader
