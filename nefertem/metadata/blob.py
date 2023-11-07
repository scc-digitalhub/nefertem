"""
BlobLog module.
"""
from nefertem.metadata._base import Metadata


class BlobLog(Metadata):
    """
    Object logged to backend.

    Attributes
    ----------
    contents : dict
        Blob of metadata to log.
    """

    def __init__(self, run_id: str, experiment_name: str, nefertem_version: str, contents: dict) -> None:
        """
        Constructor.
        """
        super().__init__(run_id, experiment_name, nefertem_version)
        self.contents = contents

    def to_dict(self) -> dict:
        """
        Render the object as a dictionary.

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
