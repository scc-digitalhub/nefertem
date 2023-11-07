"""
Run handler module.
"""
from typing import Any

from nefertem_profiling.metadata.report import NefertemProfile

from nefertem.metadata.blob import BlobLog
from nefertem.run.run import Run
from nefertem.utils.commons import RESULT_FRAMEWORK, RESULT_NEFERTEM, RESULT_RENDERED


class RunProfiling(Run):
    """
    Run profiling extension.

    Methods
    -------
    profile
        Execute profile profiling on resources.
    profile_framework
        Execute profile profiling on resources with profiling frameworks.
    profile_nefertem
        Execute profile profiling on resources with Nefertem.
    log_profile
        Log NefertemProfiles.
    persist_profile
        Persist frameworks profiles.
    """

    def profile_framework(self) -> list[Any]:
        """
        Execute profiling on resources with profiling frameworks.

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        profiles = self.run_handler.get_item(RESULT_FRAMEWORK)
        if profiles:
            return profiles

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(RESULT_FRAMEWORK)

    def profile_nefertem(self) -> list[NefertemProfile]:
        """
        Execute profiling on resources with Nefertem.

        Returns
        -------
        list[NefertemProfile]
            Return a list of NefertemProfile.

        """
        profiles = self.run_handler.get_item(RESULT_NEFERTEM)
        if profiles:
            return profiles

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(RESULT_NEFERTEM)

    def profile(self) -> tuple[list[Any], list[NefertemProfile]]:
        """
        Execute profiling on resources.

        Returns
        -------
        Any
            Return a list of NefertemProfile and the corresponding list of framework results.

        """
        return self.profile_framework(), self.profile_nefertem()

    def log_profile(self) -> None:
        """
        Log NefertemProfiles.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(RESULT_NEFERTEM):
            metadata = BlobLog(*self._get_base_args(), obj.to_dict()).to_dict()
            self._log_metadata(metadata, "profile")

    def persist_profile(self) -> None:
        """
        Persist frameworks profiles.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(RESULT_RENDERED):
            self._persist_artifact(obj.object, self._render_artifact_name(obj.filename))
