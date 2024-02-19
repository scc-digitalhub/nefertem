"""
DataReader registry.
"""
from __future__ import annotations

from nefertem_core.utils.commons import FILE_READER, NATIVE_READER


class ReaderRegistry(dict):
    def register(self, name: str, module: str, class_name: str) -> None:
        """
        Register a reader.

        Parameters
        ----------
        name : str
            Reader name.
        module : str
            Reader module.
        class_name : str
            Reader class name.

        Returns
        -------
        None
        """
        self[name] = [module, class_name]


reader_registry = ReaderRegistry()
reader_registry.register(FILE_READER, "nefertem_core.readers.objects.file", "FileReader")
reader_registry.register(NATIVE_READER, "nefertem_core.readers.objects.native", "NativeReader")
