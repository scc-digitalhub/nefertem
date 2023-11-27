"""
DataReader registry.
"""
from __future__ import annotations

from nefertem.utils.commons import FILE_READER, NATIVE_READER


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
reader_registry.register(FILE_READER, "nefertem.readers.objects.file", "FileReader")
reader_registry.register(NATIVE_READER, "nefertem.readers.objects.native", "NativeReader")
