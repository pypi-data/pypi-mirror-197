from .domain import Release, Version, ReleaseType
from .infrastructure_api import FileHandler

class VersionRepository():

    def __init__(self, file):
        self.file = file
        self.file_handler = None
    
    def load_file(self):
        self.file_handler = FileHandler.from_file_path(self.file)
        return self.file_handler

    def write_file(self, version_string):
        if self.file_handler is None:
            raise Exception('Version was not created by load_file method.')        
        else:
            self.file_handler.write(version_string)
    
    def parse_file(self):
        version_list, is_snapshot = self.file_handler.parse()
        return version_list, is_snapshot
    
    def get_version(self) -> Version:

        self.file_handler = self.load_file()
        version_list, is_snapshot = self.parse_file()
        version = Version(self.file, version_list)
        version.is_snapshot = is_snapshot
        
        return version

class ReleaseTypeRepository():
    def __init__(self, git_api, environment_api=None):
        self.git_api = git_api

    def get_release_type(self):
        latest_commit = self.git_api.get_latest_commit()

        if ReleaseType.MAJOR.name in latest_commit.upper():
            return ReleaseType.MAJOR
        elif ReleaseType.MINOR.name in latest_commit.upper():
            return ReleaseType.MINOR
        elif ReleaseType.PATCH.name in latest_commit.upper():
            return ReleaseType.PATCH
        elif ReleaseType.SNAPSHOT.name in latest_commit.upper():
            return ReleaseType.SNAPSHOT
        else:
            return None

class ReleaseRepository():
    def __init__(self, version_repository: VersionRepository, release_type_repository: ReleaseTypeRepository, main_branch: str):
        self.version_repository = version_repository
        self.release_type_repository = release_type_repository
        self.main_branch = main_branch

    def get_release(self) -> Release:
        return Release(self.release_type_repository.get_release_type(), self.version_repository.get_version(), self.main_branch)
