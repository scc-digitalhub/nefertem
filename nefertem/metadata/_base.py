"""
Metadata module.
"""
from abc import abstractmethod


class Metadata:
    """
    Base class for metadata objects.

    Attributes
    ----------
    run_id : str
        Run id.
    experiment_name : str
        Experiment name.
    nefertem_version : str
        Version of the library.
    """

    def __init__(self, run_id: str, experiment_name: str, nefertem_version: str) -> None:
        """
        Constructor.
        """
        self.run_id = run_id
        self.experiment_name = experiment_name
        self.nefertem_version = nefertem_version

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Render the object as a dictionary.
        """

    def __repr__(self) -> str:
        return str(self.to_dict())
