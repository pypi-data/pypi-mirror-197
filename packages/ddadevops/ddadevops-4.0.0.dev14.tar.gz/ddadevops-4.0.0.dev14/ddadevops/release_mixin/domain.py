from enum import Enum
from pathlib import Path

class ReleaseType(Enum):
    MAJOR = 0
    MINOR = 1
    PATCH = 2
    SNAPSHOT = 3
    BUMP = None

class Version():

    def __init__(self, id: Path, version_list: list):
        self.id = id
        self.version_list = version_list
        self.version_string = None
        self.is_snapshot = None

    def increment(self, release_type: ReleaseType):
        self.is_snapshot = False
        match release_type:
            case ReleaseType.BUMP:
                self.is_snapshot = True
                self.version_list[ReleaseType.PATCH.value] += 1
            case ReleaseType.SNAPSHOT:
                self.is_snapshot = True
            case ReleaseType.PATCH:
                self.version_list[ReleaseType.PATCH.value] += 1
            case ReleaseType.MINOR:
                self.version_list[ReleaseType.PATCH.value] = 0
                self.version_list[ReleaseType.MINOR.value] += 1
            case ReleaseType.MAJOR:
                self.version_list[ReleaseType.PATCH.value] = 0
                self.version_list[ReleaseType.MINOR.value] = 0
                self.version_list[ReleaseType.MAJOR.value] += 1
            case None:
                raise Exception("Release Type was not set!")

    def get_version_string(self) -> str:
        self.version_string = ".".join([str(x) for x in self.version_list])
        if self.is_snapshot:
            self.version_string += "-SNAPSHOT"
        return self.version_string

    def create_release_version(self, release_type: ReleaseType):
        release_version = Version(self.id, self.version_list.copy())
        release_version.is_snapshot = self.is_snapshot
        release_version.increment(release_type)
        return release_version

    def create_bump_version(self):
        bump_version = Version(self.id, self.version_list.copy())
        bump_version.is_snapshot = self.is_snapshot
        bump_version.increment(ReleaseType.BUMP)
        return bump_version

class Release():
    def __init__(self, release_type: ReleaseType, version: Version, current_branch: str):
        self.release_type = release_type
        self.version = version
        self.current_branch = current_branch

    def release_version(self):
        return self.version.create_release_version(self.release_type)

    def bump_version(self):
        return self.release_version().create_bump_version()

    def validate(self, main_branch):
        result = []
        if self.release_type is not None and main_branch != self.current_branch:
            result.append(f"Releases are allowed only on {main_branch}")
        return result

    def is_valid(self, main_branch):
        return self.validate(main_branch).count < 1
