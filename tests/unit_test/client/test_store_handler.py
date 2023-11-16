# from pathlib import Path

# import pytest

# from nefertem.client.store_handler import (
#     StoreHandler,
# )
# from nefertem.stores.artifact.objects.base import InputStore
# from nefertem.stores.artifact.objects.dummy import DummyInputStore
# from nefertem.stores.metadata.objects.base import OutputStore
# from nefertem.stores.metadata.objects.dummy import DummyOutputStore
# from nefertem.utils.commons import DUMMY
# from nefertem.utils.exceptions import StoreError


# class TestStoreHandler:
#     def test_setup(self, temp_data):
#         handler = StoreHandler(tmp_dir=temp_data)
#         assert isinstance(handler.get_md_store(), OutputStore)
#         assert isinstance(handler.get_art_store(DUMMY), InputStore)
#         assert isinstance(handler.get_def_store(), InputStore)

#     def test_add_metadata_store(self, temp_data, mds_cfg):
#         handler = StoreHandler(tmp_dir=temp_data)
#         handler._add_metadata_store(mds_cfg)
#         assert isinstance(handler.get_md_store(), OutputStore)

#     def test_add_artifact_store(self, temp_data, st_loc1_cfg):
#         handler = StoreHandler(tmp_dir=temp_data)
#         handler.add_artifact_store(st_loc1_cfg)
#         assert isinstance(handler.get_art_store(st_loc1_cfg.name), InputStore)
#         with pytest.raises(StoreError):
#             handler.add_artifact_store(st_loc1_cfg)

#     def test_update_default_store(self, temp_data, st_loc1_cfg, st_loc2_cfg):
#         handler = StoreHandler(store=st_loc1_cfg, tmp_dir=temp_data)
#         assert handler._update_default_store() is None

#         with pytest.raises(StoreError):
#             handler = StoreHandler(store=st_loc1_cfg, tmp_dir=temp_data)
#             st_loc2_cfg.isDefault = True
#             handler.add_artifact_store(st_loc2_cfg)
#             handler._update_default_store()

#         with pytest.raises(StoreError):
#             st_loc1_cfg.isDefault = False
#             st_loc2_cfg.isDefault = False
#             handler = StoreHandler(store=[st_loc1_cfg, st_loc2_cfg], tmp_dir=temp_data)
#             handler._update_default_store()

#     def test_get_md_store(self, temp_data):
#         assert isinstance(StoreHandler(tmp_dir=temp_data).get_md_store(), DummyOutputStore)

#     def test_get_art_store(self, temp_data):
#         assert isinstance(
#             StoreHandler(tmp_dir=temp_data).get_art_store(DUMMY),
#             DummyInputStore,
#         )

#     def test_get_def_store(self, temp_data):
#         assert isinstance(StoreHandler(tmp_dir=temp_data).get_def_store(), DummyInputStore)

#     def test_get_all_art_stores(self, temp_data):
#         assert isinstance(StoreHandler(tmp_dir=temp_data).get_all_art_stores(), list)

#     def test_clean_all(self, tmp_path_factory):
#         tmp = str(tmp_path_factory.mktemp("test"))
#         StoreHandler(tmp_dir=tmp).clean_all()
#         assert not Path(tmp).is_dir()

#     def test_clean_temp_path_store_cache(self, temp_data, st_loc1_cfg):
#         handler = StoreHandler(store=st_loc1_cfg, tmp_dir=temp_data)
#         store = handler.get_art_store(st_loc1_cfg.name)
#         store.resource_paths.registry = "test"
#         assert store.resource_paths.registry == "test"
#         handler._clean_temp_path_store_cache()
#         assert store.resource_paths.registry == {}


# # Metadata store config
# @pytest.fixture
# def mds_cfg(local_md_store_cfg):
#     return local_md_store_cfg


# # Artifact store config 1
# @pytest.fixture
# def st_loc1_cfg(local_store_cfg):
#     return local_store_cfg


# # Artifact store config 2
# @pytest.fixture
# def st_loc2_cfg(local_store_cfg_2):
#     return local_store_cfg_2


# # Store Registry
# @pytest.fixture()
# def registry():
#     return StoreRegistry()


# # Metadata store object
# @pytest.fixture()
# def md_st(store_builder, mds_cfg):
#     return store_builder.build(mds_cfg)


# # Artifact store object 1
# @pytest.fixture()
# def st_1(store_builder, st_loc1_cfg):
#     return store_builder.build(st_loc1_cfg)


# # Artifact store object 2
# @pytest.fixture()
# def st_2(store_builder, st_loc2_cfg):
#     return store_builder.build(st_loc2_cfg)
