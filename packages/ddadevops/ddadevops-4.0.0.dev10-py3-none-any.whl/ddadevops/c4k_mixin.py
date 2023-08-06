import deprecation
from .domain import C4k, DnsRecord
from .devops_build import DevopsBuild
from .credential import gopass_field_from_path, gopass_password_from_path
from .infrastructure import ProjectRepository, FileApi, ExecutionApi


@deprecation.deprecated(deprecated_in="3.2")
# create objects direct instead
def add_c4k_mixin_config(
    config,
    c4k_config_dict,
    c4k_auth_dict,
    executabel_name=None,
    grafana_cloud_user=None,
    grafana_cloud_password=None,
    grafana_cloud_url="https://prometheus-prod-01-eu-west-0.grafana.net/api/prom/push",
):
    if not grafana_cloud_user:
        grafana_cloud_user = gopass_field_from_path(
            "server/meissa/grafana-cloud", "grafana-cloud-user"
        )
    if not grafana_cloud_password:
        grafana_cloud_password = gopass_password_from_path(
            "server/meissa/grafana-cloud"
        )
    c4k_auth_dict.update(
        {
            "mon-auth": {
                "grafana-cloud-user": grafana_cloud_user,
                "grafana-cloud-password": grafana_cloud_password,
            }
        }
    )
    c4k_config_dict.update({"mon-cfg": {"grafana-cloud-url": grafana_cloud_url}})
    config.update(
        {
            "C4kMixin": {
                "executabel_name": executabel_name,
                "config": c4k_config_dict,
                "auth": c4k_auth_dict,
            }
        }
    )
    return config


#TODO: refactor this to C4kBuild
class C4kMixin(DevopsBuild):
    def __init__(self, project, config):
        super().__init__(project, config)
        self.execution_api = ExecutionApi()
        c4k_build = C4k(config)
        self.repo.set_c4k(self.project, c4k_build)

    def update_runtime_config(self, dns_record: DnsRecord):
        c4k_build = self.repo.get_c4k(self.project)
        c4k_build.update_runtime_config(dns_record)
        self.repo.set_c4k(self.project, c4k_build)

    def write_c4k_config(self):
        build = self.repo.get_devops(self.project)
        c4k_build = self.repo.get_c4k(self.project)
        path = build.build_path() + "/out_c4k_config.yaml"
        self.file_api.write_yaml_to_file(path, c4k_build.config())

    def write_c4k_auth(self):
        build = self.repo.get_devops(self.project)
        c4k_build = self.repo.get_c4k(self.project)
        path = build.build_path() + "/out_c4k_auth.yaml"
        self.file_api.write_yaml_to_file(path, c4k_build.c4k_mixin_auth)

    def c4k_apply(self, dry_run=False):
        build = self.repo.get_devops(self.project)
        c4k_build = self.repo.get_c4k(self.project)
        return self.execution_api.execute(c4k_build.command(build), dry_run)
