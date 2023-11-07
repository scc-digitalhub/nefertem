from nefertem.metadata._base import Metadata


class Artifact(Metadata):
    def __init__(self, run_id: str, experiment_name: str, nefertem_version: str, uri: str, name: str) -> None:
        """
        Constructor.
        """
        super().__init__(run_id, experiment_name, nefertem_version)
        self.uri = uri
        self.name = name

    def to_dict(self) -> dict:
        return self.__dict__
