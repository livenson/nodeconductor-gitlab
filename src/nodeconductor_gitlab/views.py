from __future__ import unicode_literals

from nodeconductor.core import exceptions as core_exceptions
from nodeconductor.structure import views as structure_views

from . import ResourceType, models, serializers


class GitLabServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.GitLabService.objects.all()
    serializer_class = serializers.ServiceSerializer
    import_serializer_class = serializers.GroupImportSerializer

    def get_import_context(self):
        return {'resource_type': self.request.query_params.get('resource_type')}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            resource_type = self.request.data.get('type')
            if resource_type == ResourceType.GROUP:
                return serializers.GroupImportSerializer
            elif resource_type == ResourceType.PROJECT:
                return serializers.ProjectImportSerializer
        return super(GitLabServiceViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        """
        To get list of GitLab resources that can be linked to NodeConductor - issue GET request against
        **/api/gitlab/<service_uuid>/link/**.

        Available filters:

        ?resource_type - name of gilab resource: 'project' or 'group'. Optional, if not defined -
        endpoint will return all available resources.
        """
        return super(GitLabServiceViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        To link GitLab resource to NodeConductor - issue POST request against **/api/gitlab/<service_uuid>/link/**.

        Request example:

        .. code-block:: http

            POST /api/gitlab/<service_uuid>/link/ HTTP/1.1
            Content-Type: application/json
            Accept: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "project": "http://example.com/api/projects/73c7807a577145f5a3a3f8d9ecc1f2ac/",
                "backend_id": "45",
                "type": "project"
            }
        """
        return super(GitLabServiceViewSet, self).create(request, *args, **kwargs)


class GitLabServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.GitLabServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer


class BaseGitLabResourceViewSet(structure_views.BaseOnlineResourceViewSet):

    def check_destroy(self, resource):
        pass

    def perform_managed_resource_destroy(self, resource, force=False):
        self.check_destroy(resource)
        super(BaseGitLabResourceViewSet, self).perform_managed_resource_destroy(resource, force=force)


class GroupViewSet(BaseGitLabResourceViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer

    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(
            resource,
            path=serializer.validated_data['path'])

    def check_destroy(self, resource):
        if resource.projects.count():
            raise core_exceptions.IncorrectStateException(
                "This group contains projects. Only empty group can be deleted.")


class ProjectViewSet(BaseGitLabResourceViewSet):
    """
    To get GitLab project commits count - check project "commit_count" quota. Quota history can be used as commits count
    historical data. Look "Quotas" section for more details.
    """
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(
            resource,
            wiki_enabled=serializer.validated_data.get('wiki_enabled', False),
            issues_enabled=serializer.validated_data.get('issues_enabled', False),
            snippets_enabled=serializer.validated_data.get('snippets_enabled', False),
            merge_requests_enabled=serializer.validated_data.get('merge_requests_enabled', False))
