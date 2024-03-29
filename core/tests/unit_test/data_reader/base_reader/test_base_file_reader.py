import pytest
from nefertem_core.utils.commons import FILE_READER


def test_fetch_data(reader, data_path_csv):
    path = reader.fetch_data(data_path_csv)
    assert path == data_path_csv


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def data_reader():
    return FILE_READER
