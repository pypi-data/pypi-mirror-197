import deprecation
from typing import List
from .common import (
    Validateable,
    DnsRecord,
    Devops,
)

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
