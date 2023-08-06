import deprecation
from typing import List
from .python_util import filter_none


class Validateable:
    def __validate_is_not_empty__(self, field_name: str) -> List[str]:
        value = self.__dict__[field_name]
        if value is None or value == "":
            return [f"Field '{field_name}' may not be empty."]
        else:
            return []

    def validate(self) -> List[str]:
        return []

    def is_valid(self) -> bool:
        return len(self.validate()) < 1


class DnsRecord(Validateable):
    def __init__(self, fqdn, ipv4=None, ipv6=None):
        self.fqdn = fqdn
        self.ipv4 = ipv4
        self.ipv6 = ipv6

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("fqdn")
        if (not self.ipv4) and (not self.ipv6):
            result.append("ipv4 & ipv6 may not both be empty.")
        return result


class Devops(Validateable):
    def __init__(
        self, stage, project_root_path, module, name=None, build_dir_name="target"
    ):
        self.stage = stage
        self.name = name
        self.project_root_path = project_root_path
        self.module = module
        if not name:
            self.name = module
        self.build_dir_name = build_dir_name
        # Deprecated - no longer use generic stack ...
        self.stack = {}

    @deprecation.deprecated(deprecated_in="3.2")
    # use .name instead
    def name(self):
        return self.name

    def build_path(self):
        path = [self.project_root_path, self.build_dir_name, self.name, self.module]
        return "/".join(filter_none(path))

    def __put__(self, key, value):
        self.stack[key] = value

    def __get__(self, key):
        return self.stack[key]

    def __get_keys__(self, keys):
        result = {}
        for key in keys:
            result[key] = self.__get__(key)
        return result


class Docker(Validateable):
    def __init__(
        self,
        dockerhub_user,
        dockerhub_password,
        devops: Devops,
        build_dir_name="target",
        use_package_common_files=True,
        build_commons_path=None,
        docker_build_commons_dir_name="docker",
        docker_publish_tag=None,
    ):
        self.dockerhub_user = dockerhub_user
        self.dockerhub_password = dockerhub_password
        self.use_package_common_files = use_package_common_files
        self.build_commons_path = build_commons_path
        self.docker_build_commons_dir_name = docker_build_commons_dir_name
        self.docker_publish_tag = docker_publish_tag
        self.devops = devops

    def docker_build_commons_path(self):
        list = [self.build_commons_path, self.docker_build_commons_dir_name]
        return "/".join(filter_none(list)) + "/"


class C4k(Validateable):
    def __init__(self, config: map):
        tmp_executabel_name = config["C4kMixin"]["executabel_name"]
        if not tmp_executabel_name:
            tmp_executabel_name = config["module"]
        self.executabel_name = tmp_executabel_name
        self.c4k_mixin_config = config["C4kMixin"]["config"]
        self.c4k_mixin_auth = config["C4kMixin"]["auth"]
        tmp = self.c4k_mixin_config["mon-cfg"]
        tmp.update({"cluster-name": config["module"], "cluster-stage": config["stage"]})
        self.c4k_mixin_config.update({"mon-cfg": tmp})
        self.dns_record = None

    # TODO: these functions should be located at TerraformBuild later on.
    def update_runtime_config(self, dns_record: DnsRecord):
        self.dns_record = dns_record

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("fqdn")
        if self.dns_record:
            result += self.dns_record.validate()
        return result

    def config(self):
        fqdn = self.dns_record.fqdn
        self.c4k_mixin_config.update({"fqdn": fqdn})
        return self.c4k_mixin_config

    def command(self, build: Devops):
        module = build.module
        build_path = build.build_path()
        config_path = f"{build_path}/out_c4k_config.yaml"
        auth_path = f"{build_path}/out_c4k_auth.yaml"
        output_path = f"{build_path}/out_{module}.yaml"
        return f"c4k-{self.executabel_name}-standalone.jar {config_path} {auth_path} > {output_path}"
