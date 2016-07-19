from nodeconductor.structure import perms as structure_perms


PERMISSION_LOGICS = (
    ('nodeconductor_gitlab.GitLabService', structure_perms.service_permission_logic),
    ('nodeconductor_gitlab.GitLabServiceProjectLink', structure_perms.service_project_link_permission_logic),
    ('nodeconductor_gitlab.Project', structure_perms.resource_permission_logic),
    ('nodeconductor_gitlab.Group', structure_perms.resource_permission_logic),
)
