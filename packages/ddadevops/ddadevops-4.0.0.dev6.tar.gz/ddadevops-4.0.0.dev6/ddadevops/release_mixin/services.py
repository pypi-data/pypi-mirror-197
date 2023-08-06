from .infrastructure import ReleaseRepository
from .infrastructure_api import GitApi
from .domain import Version, Release

class PrepareReleaseService():

    def __init__(self, release_repo: ReleaseRepository):
        self.release_repo = release_repo
        self.release = release_repo.get_release()
        self.git_api = GitApi()

    def __write_and_commit_version(self, version: Version, commit_message: str):
        self.release.validate(self.release_repo.main_branch)

        self.release_repo.version_repository.write_file(version.get_version_string())
        self.git_api.add_file(self.release_repo.version_repository.file)
        self.git_api.commit(commit_message)

    def write_and_commit_release(self):
        self.__write_and_commit_version(self.release.release_version(), commit_message=f'Release v{self.release.release_version().get_version_string()}')

    def write_and_commit_bump(self):
        self.__write_and_commit_version(self.release.bump_version(), commit_message='Version bump')

class TagAndPushReleaseService():

    def __init__(self, git_api: GitApi):
        self.git_api = git_api

    def tag_release(self, release: Release):
        annotation = 'v' + release.version.get_version_string()
        message = 'Release ' + annotation
        self.git_api.tag_annotated(annotation, message, 1)

    def push_release(self):
        self.git_api.push()
