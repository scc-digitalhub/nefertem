"""
Blob module.
"""
from __future__ import annotations

from nefertem.utils.commons import NEFERTEM_VERSION


class Blob:
    """
    Object logged to backend.

    Attributes
    ----------
    run_id : str
        Run id.
    experiment_name : str
        Experiment name.
    contents : dict
        Blob of metadata to log.
    """

    def __init__(self, run_id: str, experiment_name: str, contents: dict) -> None:
        """
        Constructor.
        """
        self.run_id = run_id
        self.experiment_name = experiment_name
        self.contents = contents
        self.nefertem_version = NEFERTEM_VERSION

    def to_dict(self) -> dict:
        """
        Render the object as a dictionary.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        return self.__dict__
