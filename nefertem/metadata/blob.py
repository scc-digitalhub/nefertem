"""
BlobLog module.
"""
from dataclasses import dataclass

from nefertem.metadata.base import Metadata


@dataclass
class BlobLog(Metadata):
    """
    Object logged to backend.

    Attributes
    ----------
    run_id : str
        Run id.
    experiment_name : str
        Experiment name.
    nefertem_version : str
        Version of the library.
    contents : dict
        Blob of metadata to log.
    """

    run_id: str
    experiment_name: str
    nefertem_version: str
    contents: dict

    def to_dict(self) -> dict:
        """
        Override the method to_dict of the Metadata class.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        return {
            "run_id": self.run_id,
            "experiment_name": self.experiment_name,
            "nefertem_version": self.nefertem_version,
            **self.contents,
        }
