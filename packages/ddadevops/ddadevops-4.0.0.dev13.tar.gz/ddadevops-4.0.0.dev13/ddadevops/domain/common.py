import deprecation
from typing import List

def filter_none(list_to_filter):
    return [x for x in list_to_filter if x is not None]

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
