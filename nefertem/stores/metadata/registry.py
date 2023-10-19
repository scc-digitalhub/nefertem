"""
MetadataStore registry.
"""
from nefertem.stores.metadata.dummy_metadata_store import DummyMetadataStore
from nefertem.stores.metadata.local_metadata_store import LocalMetadataStore
from nefertem.utils.commons import STORE_DUMMY, STORE_LOCAL

MD_STORES = {
    STORE_LOCAL: LocalMetadataStore,
    STORE_DUMMY: DummyMetadataStore,
}
