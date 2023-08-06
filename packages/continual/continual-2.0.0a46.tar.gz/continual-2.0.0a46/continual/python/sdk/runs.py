from __future__ import annotations
import time
from threading import Thread
from typing import List, Optional, Type
import atexit
import sys
from types import TracebackType
import traceback
from continual.python.sdk.artifacts import ArtifactsManager
from continual.python.sdk.batchpredictions import BatchPredictionManager

# hide data profiles until futher review
# from continual.python.sdk.data_profiles import DataProfilesManager
from continual.python.sdk.dataset_version_assignments import (
    DatasetVersionAssignmentManager,
)
from continual.python.sdk.dataset_versions import DatasetVersionManager
from continual.python.sdk.events import EventManager

# hide experiments until futher review
# from continual.python.sdk.experiments import ExperimentManager
from continual.python.sdk.metrics import MetricsManager
from continual.python.sdk.model_versions import ModelVersionManager
from continual.python.sdk.models import ModelManager
from continual.python.sdk.datasets import DatasetManager
from continual.python.sdk.promotions import PromotionManager

from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager

from continual.python.sdk.metadata import MetadataManager
from continual.python.sdk.checks import ChecksManager
from continual.python.sdk.contexts import (
    GitContext,
    CicdRunnerContext,
    GitProviderContext,
    SdlcReviewContext,
)
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime


class RunManager(Manager):
    """Manages run resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/runs/{run}"

    def create(
        self,
        id: Optional[str] = None,
        description: Optional[str] = None,
        heartbeat_interval: Optional[int] = 5,
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: Optional[bool] = False,
    ) -> Run:
        """Create Run.

        New runs are identified by a unique run id that is
        generated from the display name.  To set a run id explicitly,
        you can pass `id`.  However run ids are globally unique across
        all projects.

        Arguments:
            id: User-defined run id.
            description: A string description of the run
            heartbeat_interval: integer number of seconds to wait between run heartbeats to
                Continual endpoint
            tags: A dict of str: str tags to associate with the run
            replace_if_exists: If true, will return existing run if it exists, otherwise will raise
                an exception.

        Returns:
            A new Run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> client.runs.create(description='Example run') # Assuming project is already set on client
            <Run object {'name': 'projects/example-proj/environments/production/runs/ceeflaq5lsrhv5c4skig',
            'description': 'Example run', 'author': 'sessions/CR6gwrc8vJuioj4iUc3VHA',
            'create_time': '2022-12-16T23:09:31.501970Z', 'update_time': '2022-12-16T23:09:31.501970Z',
            'last_heartbeat': '2022-12-16T23:09:31.517043Z', 'heartbeat_interval': '5', 'state': 'ACTIVE',
            'error_message': ''}>
            >>> proj = ... # Assume project `proj` has been created
            >>> env = proj.environments.create('example-env')
            >>> env.runs.create(description='Example run') # Can also create a run from an environment
            <Run object {'name': 'projects/example-proj/environments/example-env/runs/cxeglaq5ltrhm2c8skfa',
            'description': 'Example run', 'author': 'sessions/CR6gwrc8vJuioj4iUc3VHA',
            'create_time': '2022-12-16T23:09:31.501970Z', 'update_time': '2022-12-16T23:09:31.501970Z',
            'last_heartbeat': '2022-12-16T23:09:31.517043Z', 'heartbeat_interval': '5', 'state': 'ACTIVE',
            'error_message': ''}>
        """
        if tags:
            assert all(
                [isinstance(k, str) and isinstance(v, str) for k, v in tags.items()]
            ), ValueError("Tags must be a dict of str: str")

        run = Run(
            description=description,
            heartbeat_interval=heartbeat_interval,
            tags=tags,
            current_run="",
        )
        self._set_contexts(run)

        req = management_pb2.CreateRunRequest(
            parent=self.parent,
            run_id=id,
            run=run.to_proto(),
            replace_if_exists=replace_if_exists,
        )

        resp = self.client._management.CreateRun(req)
        run = Run.from_proto(resp, client=self.client, current_run=resp.name)
        run.begin()
        return run

    def get(self, id: str) -> Run:
        """Get run.

        Arguments:
            id: Run name or id.

        Returns
            A run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> client.runs.get('ceeflaq5lsrhv5c4skig')
            <Run object {'name': 'projects/example-proj/environments/production/runs/ceeflaq5lsrhv5c4skig',
            'description': 'Example run', 'author': 'sessions/CR6gwrc8vJuioj4iUc3VHA',
            'create_time': '2022-12-16T23:09:31.501970Z', 'update_time': '2022-12-16T23:09:31.501970Z',
            'last_heartbeat': '2022-12-16T23:09:31.517043Z', 'heartbeat_interval': '5', 'state': 'ACTIVE',
            'error_message': ''}>
        """

        req = management_pb2.GetRunRequest(name=self.name(id))
        run = self.client._management.GetRun(req)
        return Run.from_proto(run, client=self.client, current_run=run.name)

    def get_check_summary(self, id: str) -> types.RunCheckSummary:
        """Get check summary.

        Arguments:
            id: Run name or id.

        Returns
            A check summary for all resource checks made during the run id.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> client.runs.get_check_summary("ceh47hlvn3ddnpoaa77g")
            <RunCheckSummary object {'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'checks': [{'name': 'projects/test_project/environments/production/datasets/test_ds/versions/ceh47hlvn3ddnpoaa7bg/checks/ceh47hlvn3ddnpoaa7hg', 'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'group_name': 'train', 'success': True, 'duration': 12.5, 'data': '{}', 'errors': ['test error'], 'warnings': ['test warning'], 'summary': 'No class imbalance detected', 'artifact_name': 'flowers.csv', 'create_time': '2022-12-20T23:22:46.708395Z', 'display_name': 'Check Class Imbalance', 'state': 'PASS', 'infos': []}, {'name': 'projects/test_project/environments/production/datasets/test_ds/versions/ceh47hlvn3ddnpoaa7bg/checks/ceh47hlvn3ddnpoaa7h0', 'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'group_name': 'train', 'duration': 15.4, 'data': '{}', 'errors': ['test error'], 'infos': ['test infos'], 'summary': 'Found duplicate indices in dataset', 'artifact_name': 'flowers.csv', 'create_time': '2022-12-20T23:22:46.698521Z', 'display_name': 'Check Duplicate Indices', 'success': False, 'state': 'PASS', 'warnings': []}, {'name': 'projects/test_project/environments/production/datasets/test_ds/versions/ceh47hlvn3ddnpoaa7bg/checks/ceh47hlvn3ddnpoaa7gg', 'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'group_name': 'test', 'success': True, 'duration': 15.4, 'data': '{}', 'warnings': ['test warning'], 'infos': ['test infos'], 'summary': 'No missing indices', 'artifact_name': 'flowers.csv', 'create_time': '2022-12-20T23:22:46.687837Z', 'display_name': 'Check Missing Index', 'state': 'PASS', 'errors': []}], 'state': 'PASS'}>
        """
        req = management_pb2.GetRunCheckSummaryRequest(name=self.name(id))
        resp = self.client._management.GetRunCheckSummary(req)
        return types.RunCheckSummary.from_proto(resp)

    def has_failed_checks(self, id: str) -> bool:
        """Return true if the run has any failed check.

        Arguments:
            id: Run name

        Returns:
            True, if there is a failed check. False, otherwise.

        Examples:
            >>> ...
        """
        req = management_pb2.GetRunCheckCountsRequest(run=self.name(id))
        resp = self.client._management.GetRunCheckCounts(req)
        resource_counts = types.CountsResponse.from_proto(resp)
        return int(resource_counts.counts.get(types.CheckOutcome.FAILED.value)) > 0

    def has_failed_state(self, id: str) -> bool:
        """Return true if the run state is failed.

        Arguments:
            id: Run name

        Returns:
            True, if the run state is failed. False, otherwise.

        Examples:
            >>> ...
        """
        run = self.get(id=self.name(id))
        return run.state == types.RunState.FAILED.value

    def has_failed_checks_or_state(self, id: str) -> bool:
        """Return true if the run state is failed or a check associated with this run fails.

        Arguments:
            id: Run name

        Returns:
            True, if the run has failed. False, otherwise.

        Examples:
            >>> ...
        """
        return self.has_failed_checks(id=id) or self.has_failed_state(id=id)

    def _heartbeat(self, run_name: str) -> Timestamp:
        """Send heartbeat for a given run name

        Arguments:
            run_name: string name of run

        Returns
            A Timestamp for the time of the heartbeat
        """
        req = management_pb2.LogRunHeartbeatRequest(name=run_name)
        return self.client._management.LogRunHeartbeat(req)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: str = None,
        default_sort_order: str = "ASC",
    ) -> List[Run]:
        """List runs.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of runs.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> prod_env = client.environments.get('production')
            >>> runs = [prod_env.runs.create(description=f'run{i}') for i in range(10)]
            >>> [r.description for r in prod_env.runs.list(page_size=10)]
            ['run0', 'run1', 'run2', 'run3', 'run4', 'run5', 'run6', 'run7', 'run8', 'run9']
            >>> [r.description for r in prod_env.runs.list(page_size=10)]
            ['run9', 'run8', 'run7', 'run6', 'run5', 'run4', 'run3', 'run2', 'run1', 'run0']
        """
        req = management_pb2.ListRunsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            default_sort_order=default_sort_order,
        )
        resp = self.client._management.ListRuns(req)
        return [
            Run.from_proto(x, client=self.client, current_run=x.name) for x in resp.runs
        ]

    def list_all(self) -> Pager[Run]:
        """List all runs.

        Pages through all runs using an iterator.

        Returns:
            A iterator of all runs.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> prod_env = client.environments.get('production')
            >>> runs = [prod_env.runs.create(description=f'run{i}') for i in range(5)]
            >>> [r.description for r in prod_env.runs.list_all()]
            ['run0', 'run1', 'run2', 'run3', 'run4']
        """

        def next_page(next_page_token):
            req = management_pb2.ListRunsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListRuns(req)
            return (
                [
                    Run.from_proto(x, client=self.client, current_run=x.name)
                    for x in resp.runs
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def update(self, run: Run, paths: List[str]):
        """
        Arguments:
            run : Updated run object
            paths: list of actual fields to update

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> prod_env = client.environments.get('production')
            >>> run = prod_env.runs.create(description='run0')
            >>> run.description = 'updated description'
            >>> prod_env.runs.update(run, ['description'])
            <Run object {'name': 'projects/test_proj_2/environments/test_env/runs/cefvjv25lsrvv8oofnl0',
            'description': 'updated description', 'author': 'sessions/dKdgYnNcYJ5tgpxd5QfQtJ',
            'create_time': '2022-12-19T05:43:24.388872Z', 'update_time': '2022-12-19T05:43:24.388872Z',
            'last_heartbeat': '2022-12-19T05:45:29.827817Z', 'heartbeat_interval': '5', 'state': 'ACTIVE',
            'error_message': ''}>
        """
        req = management_pb2.UpdateRunRequest(run=run.to_proto(), update_paths=paths)
        resp = self.client._management.UpdateRun(req)
        return Run.from_proto(resp, client=self.client, current_run=resp.name)

    def _set_contexts(self, run: Run):
        """Set execution contexts as run fields."""
        try:
            git_context = GitContext().get()
            if git_context is not None:
                run.git_context = git_context

            git_provider_context = GitProviderContext().get()
            if git_provider_context is not None:
                run.git_provider_context = git_provider_context

            cicd_runner_context = CicdRunnerContext().get()
            if cicd_runner_context is not None:
                run.cicd_runner_context = cicd_runner_context

            sdlc_review_context = SdlcReviewContext().get()
            if sdlc_review_context is not None:
                run.sdlc_review_context = sdlc_review_context

        except Exception as e:
            if self.client.config.debug:
                print(f"Error setting contexts: {e}")
                print(traceback.format_exc())


class RunExitHooks(object):
    def __init__(self):
        self.exit_code = None
        self.exception = None

    def hook(self):
        self._orig_exit = sys.exit
        ## TODO: Consider sys.__excepthook__ if other libraries also follow a similar pattern
        self._orig_excepthook = sys.excepthook
        self._orig_exc_handler = self.exc_handler
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(
        self, exc_type: Type[BaseException], exc: BaseException, tb: TracebackType
    ):
        self.exception = exc
        if isinstance(self.exception, KeyboardInterrupt):
            self.exception = "KeyboardInterrupt"
        if self._orig_excepthook:
            self._orig_excepthook(exc_type, exc, tb)


class Run(Resource, types.Run, Thread):
    """Run resource."""

    name_pattern: str = "runs/{run}"

    _manager: RunManager

    _models: ModelManager

    _model_versions: ModelVersionManager

    # hide experiments until futher review
    # _experiments: ExperimentManager

    _batch_predictions: BatchPredictionManager

    _promotions: PromotionManager

    _datasets: DatasetManager

    _dataset_versions: DatasetVersionManager

    # hide data profiles until futher review
    # _data_profiles: DataProfilesManager

    _assignments: DatasetVersionAssignmentManager

    _events: EventManager

    _metadata: MetadataManager

    _metrics: MetricsManager

    _checks: ChecksManager

    _artifacts: ArtifactsManager

    def _init(self):
        Thread.__init__(self, daemon=True)
        self._manager = RunManager(
            parent=self.parent, client=self.client, run_name=self.name
        )
        self._models = ModelManager(
            parent=self.parent, client=self.client, run_name=self.name
        )
        self._datasets = DatasetManager(
            parent=self.parent, client=self.client, run_name=self.name
        )
        self._artifacts = ArtifactsManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.name
        )

        self._checks = ChecksManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        self._events = EventManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        self._model_versions = ModelVersionManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        # hide experiments until futher review
        # self._experiments = ExperimentManager(
        #     parent=self.name, client=self.client, run_name=self.name
        # )
        self._batch_predictions = BatchPredictionManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        self._promotions = PromotionManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        self._dataset_versions = DatasetVersionManager(
            parent=self.name, client=self.client, run_name=self.name
        )
        # hide data profiles until futher review
        # self._data_profiles = DataProfilesManager(
        #     parent=self.name, client=self.client, run_name=self.name
        # )
        self._assignments = DatasetVersionAssignmentManager(
            parent=self.name, client=self.client, run_name=self.name
        )

    @property
    def models(self) -> ModelManager:
        """Model manager."""
        return self._models

    @property
    def model_versions(self) -> ModelVersionManager:
        """Model version manager."""
        return self._model_versions

    # hide experiments until futher review
    # @property
    # def experiments(self) -> ExperimentManager:
    #     """Experiment manager."""
    #     return self._experiments

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch prediction manager."""
        return self._batch_predictions

    @property
    def promotions(self) -> PromotionManager:
        """Promotion manager."""
        return self._promotions

    @property
    def datasets(self) -> DatasetManager:
        """Dataset manager."""
        return self._datasets

    @property
    def dataset_versions(self) -> DatasetVersionManager:
        """Dataset version manager."""
        return self._dataset_versions

    # hide data profiles until futher review
    # @property
    # def data_profiles(self) -> DataProfilesManager:
    #     """Data profiles manager."""
    #     return self._data_profiles

    @property
    def assignments(self) -> DatasetVersionAssignmentManager:
        """Dataset version assignment manager."""
        return self._assignments

    @property
    def events(self) -> EventManager:
        """Event manager."""
        return self._events

    @property
    def metadata(self) -> MetadataManager:
        """Metadata manager."""
        return self._metadata

    @property
    def metrics(self) -> MetricsManager:
        """Metrics manager."""
        return self._metrics

    @property
    def checks(self) -> ChecksManager:
        """Resource checks manager."""
        return self._checks

    @property
    def artifacts(self) -> ArtifactsManager:
        """Artifact manager."""
        return self._artifacts

    def begin(self):
        """Start Run.

        Starts the heartbeat thread for this run, and logs git context.
        """
        atexit.register(self._handle_exit)
        self._running = True
        self._hooks = RunExitHooks()
        self._hooks.hook()
        # Thread start
        self.start()

    def _handle_exit(self):
        if self._hooks.exit_code is not None and self._hooks.exit_code != 0:
            self.fail(f"run process exited with code [{self._hooks.exit_code}]")
        elif self._hooks.exception is not None:
            self.fail(f"run process exited with exception [{self._hooks.exception}]")
        else:
            self.complete()

    def fail(self, error_message: str):
        """Fail a Run.

        Arguments:
            error_message : The error message for the failure

        This method is called when the run has failed.
        It will stop the heartbeat thread,
        set the run state to failed, set the error message and set the completed time for the run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> prod_env = client.environments.get('production')
            >>> run = prod_env.runs.create(description='run0') # Start a run
            >>> run.fail("something when wrong")                                 # Fail the run
        """

        # if run has not already finished
        if self.state != "FAILED" and self.state != "COMPLETED":
            self.state = "FAILED"
            self.error_message = error_message
            self.complete_time = datetime.now()
            self._manager.update(
                self, paths=["state", "complete_time", "error_message"]
            )
            self._running = False

        # join if thread has started
        if self.is_alive():
            self.join()

    def complete(self):
        """Cleanup Run.

        This method is called when the run is completed.
        It will stop the heartbeat thread,
        set the run state to completed and set the completed time for the run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> prod_env = client.environments.get('production')
            >>> run = prod_env.runs.create(description='run0') # Start a run
            >>> run.complete()                                 # Complete the run
        """

        # if run has not already completed
        if self.state != "COMPLETED":
            self.state = "COMPLETED"
            self.complete_time = datetime.now()
            self._manager.update(run=self, paths=["state", "complete_time"])
            self._running = False

        # join if thread has started
        if self.is_alive():
            self.join()

    def _heartbeat(self):
        """Sends a heartbeat to the server from this run."""
        self.last_heartbeat = self._manager._heartbeat(run_name=self.name).ToDatetime()

    def set_state(self, state: str):
        """Set run state.

        Arguments:
            state: The string name of the new state

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> prod_env = client.environments.get('production')
            >>> run = prod_env.runs.create(description='run0') # Start a run
            >>> run.set_state('INACTIVE')                      # Set run state to inactive
            >>> prod_env.runs.get(run.id).state                # Get run state
            'INACTIVE'
        """
        self.state = state
        self._manager.update(self, paths=["state"])

    def get_check_summary(self):
        """Get check summary.

        Arguments:

        Returns
            A check summary for all resource checks made during this run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> run = client.runs.get("ceh47hlvn3ddnpoaa77g")
            >>> run.get_check_summary()
            <RunCheckSummary object {'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'checks': [{'name': 'projects/test_project/environments/production/datasets/test_ds/versions/ceh47hlvn3ddnpoaa7bg/checks/ceh47hlvn3ddnpoaa7hg', 'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'group_name': 'train', 'success': True, 'duration': 12.5, 'data': '{}', 'errors': ['test error'], 'warnings': ['test warning'], 'summary': 'No class imbalance detected', 'artifact_name': 'flowers.csv', 'create_time': '2022-12-20T23:22:46.708395Z', 'display_name': 'Check Class Imbalance', 'state': 'PASS', 'infos': []}, {'name': 'projects/test_project/environments/production/datasets/test_ds/versions/ceh47hlvn3ddnpoaa7bg/checks/ceh47hlvn3ddnpoaa7h0', 'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'group_name': 'train', 'duration': 15.4, 'data': '{}', 'errors': ['test error'], 'infos': ['test infos'], 'summary': 'Found duplicate indices in dataset', 'artifact_name': 'flowers.csv', 'create_time': '2022-12-20T23:22:46.698521Z', 'display_name': 'Check Duplicate Indices', 'success': False, 'state': 'PASS', 'warnings': []}, {'name': 'projects/test_project/environments/production/datasets/test_ds/versions/ceh47hlvn3ddnpoaa7bg/checks/ceh47hlvn3ddnpoaa7gg', 'run_name': 'projects/test_project/environments/production/runs/ceh47hlvn3ddnpoaa77g', 'group_name': 'test', 'success': True, 'duration': 15.4, 'data': '{}', 'warnings': ['test warning'], 'infos': ['test infos'], 'summary': 'No missing indices', 'artifact_name': 'flowers.csv', 'create_time': '2022-12-20T23:22:46.687837Z', 'display_name': 'Check Missing Index', 'state': 'PASS', 'errors': []}], 'state': 'PASS'}>
        """
        return self._manager.get_check_summary(self.name)

    def run(self):
        while True:
            if not self._running:
                break
            self._heartbeat()
            time.sleep(self.heartbeat_interval)

    def update(self, paths: List[str]) -> Run:
        """Update Run.

        Arguments:
            paths: A list of paths to be updated.

        Returns:
            An updated Run.

        Examples:
            >>> ...
        """
        return self._manager.update(paths=paths, run=self)

    def has_failed_checks(self):
        """Indicate whether a run has failed checks.

        Returns:
            True if at least a check associated with this run fails; False otherwise.

        Examples:
            >>> ...
        """
        return self._manager.has_failed_checks(self.name)

    def has_failed_state(self):
        """Indicate whether a run is in FAILED state.

        Returns:
            True if the state of a run is FAILED; False otherwise.

        Examples:
            >>> ...
        """
        return self._manager.has_failed_state(self.name)

    def has_failed_checks_or_state(self):
        """Indicate whether a run status is failed or not.

        Returns:
            True if the run fails; False otherwise.

        Examples:
            >>> ...
        """
        return self._manager.has_failed_checks_or_state(self.name)

    def add_tags(self, tags: dict[str, str]) -> Run:
        """add tags.

        Arguments:
            tags: A dictionary of tag key/tag value

        Returns:
            An updated Run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> run = client.runs.get("ceh47hlvn3ddnpoaa77g")
            >>> run.add_tag({"color": "blue", "fruit": "apple"})
        """
        for key in tags:
            self.tags[key] = tags[key]
        return self._manager.update(run=self, paths=["tags"])

    def remove_tags(self, tags: List[str]) -> Run:
        """remove tags.

        Arguments:
            tags: A list of tag keys

        Returns:
            An updated Run.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> run = client.runs.get("ceh47hlvn3ddnpoaa77g")
            >>> run.remove_tag({"color", "fruit"})
        """
        for key in tags:
            self.tags.pop(key, -1)
        return self._manager.update(run=self, paths=["tags"])
