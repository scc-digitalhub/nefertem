"""
Run module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any

from nefertem.metadata.blob import BlobLog
from nefertem.metadata.env import EnvLog
from nefertem.utils.commons import (
    INFER,
    NEFERTEM_VERSION,
    PROFILE,
    RESULT_ARTIFACT,
    RESULT_NEFERTEM,
    RESULT_RENDERED,
    STATUS_ERROR,
    STATUS_FINISHED,
    STATUS_INIT,
    STATUS_INTERRUPTED,
    VALIDATE,
)
from nefertem.utils.logger import LOGGER
from nefertem.utils.utils import get_time

if typing.TYPE_CHECKING:
    from nefertem.metadata.nefertem import NefertemProfile
    from nefertem.metadata.nefertem import NefertemReport
    from nefertem.metadata.nefertem import NefertemSchema
    from nefertem.metadata.run_info import RunInfo
    from nefertem.plugins.profiling.base import Metric
    from nefertem.plugins.utils import RenderTuple
    from nefertem.plugins.validation.base import Constraint
    from nefertem.run.run_handler import RunHandler


class Run:
    """
    Run object.
    The Run is the main interface to interact with data, metadata and
    operational framework. With the Run, you can infer, validate and
    profile resources, log and persist data and metadata.

    Methods
    -------
    infer_wrapper
        Execute schema inference on resources with inference frameworks.
    infer_nefertem
        Execute schema inference on resources with Nefertem.
    infer
        Execute schema inference on resources.
    log_schema
        Log NefertemSchemas.
    persist_schema
        Persist frameworks schemas.
    validate_wrapper
        Execute validation on resources with validation frameworks.
    validate_nefertem
        Execute validation on resources with Nefertem.
    validate
        Execute validation on resources.
    log_report
        Log NefertemReports.
    persist_report
        Persist frameworks reports.
    profile_wrapper
        Execute profiling on resources with profiling frameworks.
    profile_nefertem
        Execute profiling on resources with Nefertem.
    profile
        Execute profiling on resources.
    log_profile
        Log NefertemProfiles.
    persist_profile
        Persist frameworks profiles.
    persist_data
        Persist input data as artifacts into default store.

    """

    def __init__(self, run_info: RunInfo, run_handler: RunHandler, overwrite: bool) -> None:
        self.run_info = run_info
        self._run_handler = run_handler
        self._overwrite = overwrite

        self._filenames = {}

    ############################
    # Run methods
    ############################

    def _log_run(self) -> None:
        """
        Log run's metadata.

        Returns
        -------
        None
        """
        metadata = self._get_blob(self.run_info.to_dict())
        self._log_metadata(metadata, "run")

    def _log_env(self) -> None:
        """
        Log run's enviroment details.

        Returns
        -------
        None
        """
        metadata = self._get_blob(EnvLog().to_dict())
        self._log_metadata(metadata, "run_env")

    def _get_blob(self, blob: dict | None = None) -> dict:
        """
        Return structured blob to log.

        Returns
        -------
        dict
            Return a structured blob.
        """
        blob = blob if blob is not None else {}
        return BlobLog(self.run_info.run_id, self.run_info.experiment_name, NEFERTEM_VERSION, blob).to_dict()

    def _log_metadata(self, metadata: dict, src_type: str) -> None:
        """
        Log generic metadata.

        Returns
        -------
        None
        """
        self._run_handler.log_metadata(metadata, self.run_info.run_meta_path, src_type, self._overwrite)

    def _log_artifact(self, src_name: str | None = None) -> None:
        """
        Log artifact metadata.

        Returns
        -------
        None
        """
        metadata = self._get_blob({"uri": self.run_info.run_art_path, "name": src_name})
        self._log_metadata(metadata, "artifact")

    def _render_artifact_name(self, filename: str) -> str:
        """
        Return a modified filename to avoid overwriting in persistence.

        Returns
        -------
        str
            Return a modified filename.
        """
        self._filenames[filename] = self._filenames.get(filename, 0) + 1
        return f"{Path(filename).stem}_{self._filenames[filename]}{Path(filename).suffix}"

    def _persist_artifact(self, obj: RenderTuple) -> None:
        """
        Persist artifact in the artifact store.

        Parameters
        ----------
        obj : RenderTuple
            Tuple containing the object to persist and the filename.

        Returns
        -------
        None
        """
        src_name = self._render_artifact_name(obj.filename)
        self._run_handler.persist_artifact(obj.object, self.run_info.run_art_path, src_name)
        self._log_artifact(src_name)

    def _get_libraries(self) -> None:
        """
        Return the list of libraries used by the run.

        Returns
        -------
        None
        """
        self.run_info.run_libraries = self._run_handler.get_libs()

    ############################
    # Inferece
    ############################

    def infer_wrapper(self, parallel: bool = False, num_worker: int = 10) -> list[Any]:
        """
        Execute schema inference on resources with inference frameworks.

        Parameters
        ----------
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        schemas = self._run_handler.get_item(INFER, RESULT_ARTIFACT)
        if schemas:
            return schemas

        self._run_handler.infer(self.run_info.resources, parallel, num_worker)
        return self._run_handler.get_item(INFER, RESULT_ARTIFACT)

    def infer_nefertem(self, parallel: bool = False, num_worker: int = 10) -> list[NefertemSchema]:
        """
        Execute schema inference on resources with Nefertem.

        Parameters
        ----------
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10

        Returns
        -------
        list[NefertemSchema]
            Return a list of NefertemSchemas.

        """
        schemas = self._run_handler.get_item(INFER, RESULT_NEFERTEM)
        if schemas:
            return schemas

        self._run_handler.infer(self.run_info.resources, parallel, num_worker)
        return self._run_handler.get_item(INFER, RESULT_NEFERTEM)

    def infer(self, parallel: bool = False, num_worker: int = 10, only_nt: bool = False) -> Any:
        """
        Execute schema inference on resources.

        Parameters
        ----------
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10
        only_nt : bool
            Flag to return only the Nefertem report.

        Returns
        -------
        Any
            Return a list of NefertemSchemas and the corresponding list of framework results.
        """
        schema = self.infer_wrapper(parallel, num_worker)
        schema_nt = self.infer_nefertem(parallel, num_worker)
        if only_nt:
            return None, schema_nt
        return schema, schema_nt

    def log_schema(self) -> None:
        """
        Log NefertemSchemas.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(INFER, RESULT_NEFERTEM):
            metadata = self._get_blob(obj.to_dict())
            self._log_metadata(metadata, "schema")

    def persist_schema(self) -> None:
        """
        Persist frameworks schemas.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(INFER, RESULT_RENDERED):
            self._persist_artifact(obj)

    ############################
    # Validation
    ############################

    def validate_wrapper(
        self,
        constraints: list[Constraint],
        error_report: str | None = "partial",
        parallel: bool = False,
        num_worker: int | None = 10,
    ) -> list[Any]:
        """
        Execute validation on resources with validation frameworks.

        Parameters
        ----------
        constraints : list[Constraint]
            list of constraint to validate resources.
        error_report : str
            Flag to render the error output of the nefertem report.
            Accepts 'count', 'partial' or 'full'.
            'count' returns the errors count of the validation,
            'partial' return the errors count and a list of errors (max 100),
            'full' returns errors count and the list of all encountered errors.
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        reports = self._run_handler.get_item(VALIDATE, RESULT_ARTIFACT)
        if reports:
            return reports

        self._run_handler.validate(self.run_info.resources, constraints, error_report, parallel, num_worker)
        return self._run_handler.get_item(VALIDATE, RESULT_ARTIFACT)

    def validate_nefertem(
        self,
        constraints: list[Constraint],
        error_report: str | None = "partial",
        parallel: bool = False,
        num_worker: int | None = 10,
    ) -> list[NefertemReport]:
        """
        Execute validation on resources with Nefertem.

        Parameters
        ----------
        constraints : list[Constraint]
            list of constraint to validate resources.
        error_report : str
            Flag to render the error output of the nefertem report.
            Accepts 'count', 'partial' or 'full'.
            'count' returns the errors count of the validation,
            'partial' return the errors count and a list of errors (max 100),
            'full' returns errors count and the list of all encountered errors.
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10

        Returns
        -------
        list[NefertemReport]
            Return a list of "NefertemReport".

        """
        reports = self._run_handler.get_item(VALIDATE, RESULT_NEFERTEM)
        if reports:
            return reports

        self._run_handler.validate(self.run_info.resources, constraints, error_report, parallel, num_worker)
        return self._run_handler.get_item(VALIDATE, RESULT_NEFERTEM)

    def validate(
        self,
        constraints: list[Constraint],
        error_report: str | None = "partial",
        parallel: bool = False,
        num_worker: int | None = 10,
        only_nt: bool = False,
    ) -> Any:
        """
        Execute validation on resources.

        Parameters
        ----------
        constraints : list[Constraint]
            list of constraint to validate resources.
        error_report : str
            Flag to render the error output of the nefertem report.
            Accepts 'count', 'partial' or 'full'.
            'count' returns the errors count of the validation,
            'partial' return the errors count and a list of errors (max 100),
            'full' returns errors count and the list of all encountered errors.
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10
        only_nt : bool
            Flag to return only the Nefertem report.

        Returns
        -------
        Any
            Return a list of "NefertemReport" and the corresponding list of framework results.

        """
        report = self.validate_wrapper(constraints, error_report, parallel, num_worker)
        report_nt = self.validate_nefertem(constraints, error_report, parallel, num_worker)
        if only_nt:
            return None, report_nt
        return report, report_nt

    def log_report(self) -> None:
        """
        Log NefertemReports.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(VALIDATE, RESULT_NEFERTEM):
            metadata = self._get_blob(obj.to_dict())
            self._log_metadata(metadata, "report")

    def persist_report(self) -> None:
        """
        Persist frameworks reports.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(VALIDATE, RESULT_RENDERED):
            self._persist_artifact(obj)

    ############################
    # Profiling
    ############################

    def profile_wrapper(
        self, metrics: list[Metric] | None = None, parallel: bool = False, num_worker: int = 10
    ) -> list[Any]:
        """
        Execute profiling on resources with profiling frameworks.

        Parameters
        ----------
        metrics: list[Metric]
            Optional list of metrics to evaluate over resources.
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        profiles = self._run_handler.get_item(PROFILE, RESULT_ARTIFACT)
        if profiles:
            return profiles

        self._run_handler.profile(self.run_info.resources, metrics, parallel, num_worker)
        return self._run_handler.get_item(PROFILE, RESULT_ARTIFACT)

    def profile_nefertem(
        self, metrics: list[Metric] | None = None, parallel: bool = False, num_worker: int = 10
    ) -> list[NefertemProfile]:
        """
        Execute profiling on resources with Nefertem.

        Parameters
        ----------
        metrics: list[Metric]
            Optional list of metrics to evaluate over resources.
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10

        Returns
        -------
        list[NefertemProfile]
            Return a list of NefertemProfile.

        """
        profiles = self._run_handler.get_item(PROFILE, RESULT_NEFERTEM)
        if profiles:
            return profiles

        self._run_handler.profile(self.run_info.resources, metrics, parallel, num_worker)
        return self._run_handler.get_item(PROFILE, RESULT_NEFERTEM)

    def profile(
        self, metrics: list[Metric] | None = None, parallel: bool = False, num_worker: int = 10, only_nt: bool = False
    ) -> Any:
        """
        Execute profiling on resources.

        Parameters
        ----------
        metrics: list[Metric]
            Optional list of metrics to evaluate over resources.
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10
        only_nt : bool
            Flag to return only the Nefertem report.

        Returns
        -------
        Any
            Return a list of NefertemProfile and the corresponding list of framework results.

        """
        profile = self.profile_wrapper(metrics, parallel, num_worker)
        profile_nt = self.profile_nefertem(metrics, parallel, num_worker)
        if only_nt:
            return None, profile_nt
        return profile, profile_nt

    def log_profile(self) -> None:
        """
        Log NefertemProfiles.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(PROFILE, RESULT_NEFERTEM):
            metadata = self._get_blob(obj.to_dict())
            self._log_metadata(metadata, "profile")

    def persist_profile(self) -> None:
        """
        Persist frameworks profiles.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(PROFILE, RESULT_RENDERED):
            self._persist_artifact(obj)

    ############################
    # Data
    ############################

    def persist_data(self) -> None:
        """
        Persist input data as artifacts into default store.

        Depending on the functioning of the store object on which the artifacts are stored,
        the store will try to download the data locally.
        In the case of SQL origin, the format will be parquet.
        In the case of remote or s3 origin, the persistence format will be the same
        as the artifacts present in the storage.

        Returns
        -------
        None
        """
        self._run_handler.persist_data(self.run_info.resources, self.run_info.run_art_path)

    ############################
    # Context manager
    ############################

    def __enter__(self) -> Run:
        # Set run status
        LOGGER.info(f"Starting run {self.run_info.run_id}")
        self.run_info.begin_status = STATUS_INIT
        self.run_info.started = get_time()
        self._log_run()
        self._log_env()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.run_info.end_status = STATUS_FINISHED
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = STATUS_INTERRUPTED
        elif exc_type in (AttributeError,):
            self.run_info.end_status = STATUS_ERROR
        else:
            self.run_info.end_status = STATUS_ERROR

        self._get_libraries()
        self.run_info.finished = get_time()
        self._log_run()
        LOGGER.info("Run finished. Clean up of temp resources.")

        self._run_handler.clean_all()

    ############################
    # Dunder
    ############################

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
