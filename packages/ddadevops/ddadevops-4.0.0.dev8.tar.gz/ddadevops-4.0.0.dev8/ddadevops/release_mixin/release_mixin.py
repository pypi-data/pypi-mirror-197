from ddadevops import DevopsBuild
from .infrastructure import ReleaseRepository, ReleaseTypeRepository, VersionRepository
from .infrastructure_api import GitApi
from .services import PrepareReleaseService, TagAndPushReleaseService

def create_release_mixin_config(config_file, main_branch) -> dict:
    config = {}
    config.update(
        {'ReleaseMixin':
            {'main_branch': main_branch,
             'config_file': config_file}})
    return config

def add_versions(config, release_version, bump_version) -> dict:
    config['ReleaseMixin'].update(
        {'release_version': release_version,
         'bump_version': bump_version})
    return config

class ReleaseMixin(DevopsBuild):

    def __init__(self, project, config): # todo: create services in init, dont expose repos etc in api
        super().__init__(project, config)
        release_mixin_config = config['ReleaseMixin']                
        self.config_file = release_mixin_config['config_file']
        self.main_branch = release_mixin_config['main_branch']
        self.git_api = GitApi()
        self.release_type_repo = ReleaseTypeRepository(self.git_api) # maybe get from env?
        self.version_repo = VersionRepository(self.config_file)
        self.release_repo = ReleaseRepository(self.version_repo, self.release_type_repo, self.main_branch)

    def prepare_release(self):
        prepare_release_service = PrepareReleaseService(self.release_repo)
        prepare_release_service.write_and_commit_release()
        prepare_release_service.write_and_commit_bump()

    def tag_and_push_release(self):
        tag_and_push_release_service = TagAndPushReleaseService(self.git_api)
        tag_and_push_release_service.tag_release(self.release_repo.get_release())
        # tag_and_push_release_service.push_release()
