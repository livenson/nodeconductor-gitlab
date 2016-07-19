from nodeconductor import _get_version

__version__ = _get_version('nodeconductor_gitlab')

default_app_config = 'nodeconductor_gitlab.apps.GitLabConfig'


class ResourceType:
    GROUP = 'group'
    PROJECT = 'project'

    CHOICES = (
        (GROUP, 'Group'),
        (PROJECT, 'Projects'),
    )
