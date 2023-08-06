from __future__ import annotations
from typing import List, Optional
from continual.python.sdk.environments import EnvironmentManager
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager


class ProjectManager(Manager):
    """Manages project resources."""

    name_pattern: str = "projects/{project}"

    def create(
        self,
        organization: str,
        id: Optional[str] = "",
        display_name: Optional[str] = "",
        tags: Optional[dict[str, str]] = None,
        replace_if_exists: Optional[bool] = False,
        create_source: Optional[str] = None,
        create_source_type: Optional[str] = types.ProjectCreateSourceType.NONE,
    ) -> Project:
        """Create an project.

        New projects are identified by a unique project id that is
        generated from the display name. However project ids are globally unique across
        all organizations.

        Arguments:
            organization: Organization resource name.
            display_name: Display name.
            id : Project id.
            tags: Tags to add to the project.
            replace_if_exists: If true, replace the project if it already exists.
            create_source: The source of the project creation.
            create_source_type: The type of the source of the project creation.

        Returns:
            A new project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> client.projects.create(display_name="example-proj", organization=org.name)
            <Project object {'name': 'projects/example_proj', 'display_name': 'example-proj',
            'organization': 'organizations/ceddjsa5lsrtvmkpogm0',
            'summary': {'feature_set_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0}, '
            model_health': {'healthy_count': 0, 'unhealthy_count': 0, 'critical_count': 0}, 'feature_set_count': 0,
            'feature_set_row_count': '0', 'feature_set_bytes': '0', 'feature_count': 0, 'connection_count': 0, 'model_count': 0,
            'model_version_count': 0, 'experiment_count': '0', 'prediction_count': '0'}, 'update_time': '2022-12-15T08:25:29.713213Z',
            'create_time': '2022-12-15T08:25:29.707384Z', 'default_environment': 'projects/example_proj/environments/production'}>
        """
        if tags:
            assert all(
                [isinstance(k, str) and isinstance(v, str) for k, v in tags.items()]
            ), ValueError("Tags must be a dict of str: str")

        req = management_pb2.CreateProjectRequest(
            project=Project(
                display_name=display_name,
                organization=organization,
                tags=tags,
                current_run=self.run_name,
                create_source=create_source,
                create_source_type=create_source_type,
            ).to_proto(),
            project_id=id,
            replace_if_exists=replace_if_exists,
        )

        resp = self.client._management.CreateProject(req)
        return Project.from_proto(resp, client=self.client, current_run=self.run_name)

    def get(self, id: str) -> Project:
        """Get project.

        Arguments:
            id: Project name or id.

        Returns
            A project.

        Example:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.name)
            >>> client.projects.get(id=proj.name).display_name
            'example-proj'
        """

        req = management_pb2.GetProjectRequest(name=self.name(id))
        resp = self.client._management.GetProject(req)
        return Project.from_proto(resp, client=self.client, current_run=self.run_name)

    def list(
        self,
        page_size: Optional[int] = None,
        order_by: Optional[str] = None,
        default_sort_order: str = "ASC",
    ) -> List[Project]:
        """List projects.

        Arguments:
            page_size: Number of items to return.
            order_by: A string field name used to order list.
            latest: If true, the results are sorted in descending order, else ascending.

        Returns:
            A list of projects.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> projs = [client.projects.create(f"project-{i}", organization=org.name) for i in range(10)]
            >>> [c.display_name for client.projects.list(page_size=10)]
            ['project-0', 'project-1', 'project-2', 'project-3', 'project-4', 'project-5', 'project-6', 'project-7', 'project-8', 'project-9']
        """

        req = management_pb2.ListProjectsRequest(
            parent=self.parent,
            page_size=page_size,
            order_by=order_by,
            default_sort_order=default_sort_order,
        )
        resp = self.client._management.ListProjects(req)
        return [
            Project.from_proto(x, client=self.client, current_run=self.run_name)
            for x in resp.projects
        ]

    def list_all(self) -> Pager[Project]:
        """List all projects.

        Pages through all projects using an iterator.

        Returns:
            A iterator of all projects.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> projs = [client.projects.create(f"project-{i}", organization=org.name) for i in range(5)]
            >>> [c.display_name for client.projects.list_all()]
            ['project-0', 'project-1', 'project-2', 'project-3', 'project-4']
        """

        def next_page(next_page_token):
            req = management_pb2.ListProjectsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListProjects(req)
            return (
                [
                    Project.from_proto(x, client=self.client, current_run=self.run_name)
                    for x in resp.projects
                ],
                resp.next_page_token,
            )

        return Pager(next_page)

    def delete(self, id: str) -> None:
        """Delete an project.

        Arguments:
            id: Project name or id.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> projs = [client.projects.create(display_name=f"project-{i}", organization=org.id) for i in range(10)]
            >>> [client.projects.delete(id=proj.id)  for proj in client.projects.list_all()]
            [None, None, None, None, None, None, None, None, None, None]
            >>> len([org  for org in client.projects.list_all()])
            0
        """

        req = management_pb2.DeleteProjectRequest(name=self.name(id))
        self.client._management.DeleteProject(req)

    def update(
        self,
        paths: List[str],
        project: Project,
    ) -> Project:
        """Update Project.

        Arguments:
            paths: A list of paths to be updated.
            project: Project object containing updated fields.

        Returns:
            An updated Project.

        Examples:
            >>> ... # Assume client, project, and environment are defined.
        """

        req = management_pb2.UpdateProjectRequest(
            project=project.to_proto(),
            update_paths=paths,
            run=self.run_name,
        )
        resp = self.client._management.UpdateProject(req)
        return Project.from_proto(resp, client=self.client, current_run=self.run_name)


class Project(Resource, types.Project):
    """Project resource."""

    name_pattern: str = "projects/{project}"

    _manager: ProjectManager

    _environments: EnvironmentManager

    def _init(self):
        self._manager = ProjectManager(
            parent=self.parent, client=self.client, run_name=self.current_run
        )
        self._environments = EnvironmentManager(
            parent=self.name, client=self.client, run_name=self.current_run
        )

    @property
    def environments(self) -> EnvironmentManager:
        """Environments manager."""
        return self._environments

    def delete(self) -> None:
        """Delete project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.id)
            >>> proj.delete()
            >>> len([proj for proj in client.projects.list_all()])
            0
        """
        self._manager.delete(self.name)

    def update(self, paths: List[str] = None) -> Project:
        """Update project.

        Arguments:
            paths: A list of paths to be updated

        Returns:
            Updated project.

        Examples:
            >>> from continual import Client
            >>> client = Client() # Assuming credentials in YAML config
            >>> org = client.organizations.create(display_name="example-org")
            >>> proj = client.projects.create(display_name="example-proj", organization=org.id)
            >>> new_proj = proj.update(display_name="updated-example-proj")
            >>> new_proj.display_name
            'updated-proj-name'
        """
        return self._manager.update(project=self, paths=paths)

    def add_tags(self, tags: dict[str, str]) -> Project:
        """add tags.

        Arguments:
            tags: A dictionary of tag key/tag value

        Returns:
            An updated Project.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> project = client.projects.get("example_project")
            >>> project.add_tags({"color": "blue", "fruit": "apple"})
        """
        for key in tags:
            self.tags[key] = tags[key]
        return self._manager.update(project=self, paths=["tags"])

    def remove_tags(self, tags: List[str]) -> Project:
        """remove tags.

        Arguments:
            tags: A list of tag keys

        Returns:
            An updated Project.

        Examples:
            >>> ... # Assuming client, org and project is already authenticated
            >>> project = client.projects.get("example_project")
            >>> project.remove_tags({"color", "fruit"})
        """
        for key in tags:
            self.tags.pop(key, -1)
        return self._manager.update(project=self, paths=["tags"])
