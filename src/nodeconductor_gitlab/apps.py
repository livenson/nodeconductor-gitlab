from django.apps import AppConfig
from django.db.models import signals


class GitLabConfig(AppConfig):
    name = 'nodeconductor_gitlab'
    verbose_name = 'GitLab'
    service_name = 'GitLab'

    def ready(self):
        from nodeconductor.quotas import handlers as quotas_handlers
        from nodeconductor.structure import SupportedServices

        Project = self.get_model('Project')

        from nodeconductor_gitlab.backend import GitLabBackend
        SupportedServices.register_backend(GitLabBackend)

        signals.post_save.connect(
            quotas_handlers.add_quotas_to_scope,
            sender=Project,
            dispatch_uid='nodeconductor_gitlab.handlers.add_quotas_to_project',
        )
