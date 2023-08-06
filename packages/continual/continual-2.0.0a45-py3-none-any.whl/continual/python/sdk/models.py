from __future__ import annotations
from typing import List, Optional
from continual.python.sdk.endpoints import Endpoint, EndpointManager
from continual.python.sdk.metrics import MetricsManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.checks import ChecksManager
from continual.python.sdk.model_versions import ModelVersion, ModelVersionManager
from continual.python.sdk.promotions import Promotion, PromotionManager

from continual.python.sdk.metadata import MetadataManager


from continual.python.sdk.batchpredictions import (
    BatchPrediction,
    BatchPredictionManager,
)


class ModelManager(Manager):
    """Manages model resources."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}"

    def create(
        self,
        id: Optional[str] = "",
        display_name: Optional[str] = "",
        description: Optional[str] = "",
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: bool = False,
    ) -> Model:
        """Create model.

        Arguments:
            id: Model's name or id.
            display_name: A brief display name of this model.
            description: A brief description of this model.
            tags: A dict of tags to add to this model.
            replace_if_exists: If True, and the model exists it will be updated with the new description
                        and display name.

        Returns
            A Model.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> run.models.create(id="my_model", description="Customer churn model")
            <Model object {'name': 'projects/test_proj_4/environments/test_env/models/my_model',
            'description': 'Customer churn model', 'author': 'users/BefwyWcn6x7SNC533zfaAR',
            'id': 'my_model', 'create_time': '2022-12-19T16:31:26.638028Z',
            'update_time': '2022-12-19T16:31:26.638028Z', 'current_version': '',
            'latest_model_version': '', 'latest_batch_prediction': ''}>
        """
        if tags:
            assert all(
                [isinstance(k, str) and isinstance(v, str) for k, v in tags.items()]
            ), ValueError("Tags must be a dict of str: str")

        req = management_pb2.CreateModelRequest(
            parent=self.parent,
            model=Model(
                description=description,
                display_name=display_name,
                run=self.run_name,
                tags=tags,
                current_run=self.run_name,
            ).to_proto(),
            model_id=id,
            replace_if_exists=replace_if_exists,
        )
        resp = self.client._management.CreateModel(req)
        return Model.from_proto(resp, client=self.client, current_run=self.run_name)

    def get(self, id: str) -> Model:
        """Get model.

        Arguments:
            id: Model name or id.

        Returns
            A Model.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> model = run.models.create(id="my_model", description="Customer churn model")
            >>> run.models.get("my_model")
            <Model object {'name': 'projects/test_proj_4/environments/test_env/models/my_model',
            'description': 'Customer churn model', 'author': 'users/BefwyWcn6x7SNC533zfaAR',
            'id': 'my_model', 'create_time': '2022-12-19T16:31:26.638028Z',
            'update_time': '2022-12-19T16:31:26.638028Z', 'current_version': '',
            'latest_model_version': '', 'latest_batch_prediction': ''}>
        """
        req = management_pb2.GetModelRequest(name=self.name(id))
        resp = self.client._management.GetModel(req)
        return Model.from_proto(resp, client=self.client, current_run=self.run_name)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        default_sort_order: str = "ASC",
        all_projects: bool = False,
    ) -> List[Model]:
        """List model.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.
            all_projects: Whether to include all instances of this resource from the project or just from the current parent.

        Returns:
            A list of models.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> models = [run.models.create(id=f"my_model_{i}", description="Customer churn model") for i in range(3)]
            >>> [model.id for model in run.models.list(page_size=3)]
            ['my_model_2', 'my_model_1', 'my_model_0']
            >>> [model.id for model in run.models.list(page_size=3)]
            ['my_model_0', 'my_model_1', 'my_model_2']
        """
        req = management_pb2.ListModelsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            default_sort_order=default_sort_order,
            all_projects=all_projects,
        )
        resp = self.client._management.ListModels(req)
        return [
            Model.from_proto(x, client=self.client, current_run=self.run_name)
            for x in resp.models
        ]

    def list_all(self) -> Pager[Model]:
        """List all model.

        Pages through all model using an iterator.

        Returns:
            A iterator of all model.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
            >>> env = project.environments.get("my_environment")
            >>> run = env.runs.create("my_run")
            >>> models = [run.models.create(id=f"my_model_{i}", description="Customer churn model") for i in range(3)]
            >>> [model.id for model in run.models.list_all()]
            ['my_model_0', 'my_model_1', 'my_model_2']
        """

        def next_page(next_page_token):
            req = management_pb2.ListModelsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListModels(req)
            return (
                [
                    Model.from_proto(x, client=self.client, current_run=self.run_name)
                    for x in resp.models
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def update(
        self,
        paths: List[str],
        model: Model,
    ) -> Model:
        """Update Model.

        Arguments:
            paths: A list of paths to be updated.
            model: Model object containing updated fields.

        Returns:
            An updated Model.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
        """

        req = management_pb2.UpdateModelRequest(
            model=model.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateModel(req)
        return Model.from_proto(resp, client=self.client, current_run=self.run_name)


class Model(Resource, types.Model):
    """Model resource."""

    name_pattern: str = "projects/{project}/environments/{environment}/models/{model}"
    _manager: ModelManager
    """Model manager."""

    _model_versions: ModelVersionManager
    """ModelVersion manager."""

    _promotions: PromotionManager
    """Promotion manager."""

    _batch_predictions: BatchPredictionManager
    """Batch Prediction  manager."""

    _metadata: MetadataManager
    """Metadata Manager"""

    _metrics: MetricsManager
    """Metrics Manager"""

    _endpoints: EndpointManager
    """Endpoint Manager"""

    _checks: ChecksManager
    """Checks Manager"""

    def _init(self):
        self._manager = ModelManager(
            parent=self.parent, client=self.client, run_name=self.current_run
        )
        self._model_versions = ModelVersionManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )
        self._promotions = PromotionManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )
        self._batch_predictions = BatchPredictionManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )
        self._metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )
        self._metrics = MetricsManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )
        self._endpoints = EndpointManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )
        self._checks = ChecksManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )

    @property
    def model_versions(self) -> ModelVersionManager:
        """ModelVersion manager."""
        return self._model_versions

    @property
    def promotions(self) -> PromotionManager:
        """Promotion manager."""
        return self._promotions

    @property
    def batch_predictions(self) -> BatchPredictionManager:
        """Batch Prediction manager."""
        return self._batch_predictions

    @property
    def metadata(self) -> MetadataManager:
        """Metadata Manager"""
        return self._metadata

    @property
    def metrics(self) -> MetricsManager:
        """Metrics Manager"""
        return self._metrics

    @property
    def checks(self) -> ChecksManager:
        """Checks manager."""
        return self._checks

    @property
    def endpoints(self) -> EndpointManager:
        """Endpoint Manager"""
        return self._endpoints

    def update(self, paths: List[str]) -> Model:
        """Update Model.

        Arguments:
            paths: A list of paths to be updated.

        Returns:
            An updated Model.

        Examples:
            >>> ...
        """
        return self._manager.update(paths=paths, model=self)

    def latest_model_version(self) -> ModelVersion:
        """Get the most recently created ModelVersion.

        Returns:
            ModelVersion.
        """
        return self._model_versions._get_latest_model_version()

    def latest_promotion(self) -> Promotion:
        """Get the most recently created Promotion.

        Returns:
            Promotion.
        """
        return self._promotions._get_latest_promotion()

    def latest_batch_prediction(self) -> BatchPrediction:
        """Get the most recently created BatchPrediction.

        Returns:
            BatchPrediction.
        """
        return self._batch_predictions._get_latest_batch_prediction()

    def latest_endpoint(self) -> Endpoint:
        """Get the most recently created Endpoint.

        Returns:
            Endpoint.
        """
        return self._endpoints._get_latest_endpoint()

    def add_tags(self, tags: dict[str, str]) -> Model:
        """add tags.

        Arguments:
            tags: A dictionary of tag key/tag value

        Returns:
            An updated Model.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> model = run_obj.models.get("test_model_id")
            >>> model.add_tags({"color": "blue", "fruit": "apple"})
        """
        for key in tags:
            self.tags[key] = tags[key]
        return self._manager.update(model=self, paths=["tags"])

    def remove_tags(self, tags: List[str]) -> Model:
        """remove tags.

        Arguments:
            tags: A list of tag keys

        Returns:
            An updated Model.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> model = run_obj.models.get("test_model_id")
            >>> model.remove_tags({"color", "fruit"})
        """
        for key in tags:
            self.tags.pop(key, -1)
        return self._manager.update(model=self, paths=["tags"])
