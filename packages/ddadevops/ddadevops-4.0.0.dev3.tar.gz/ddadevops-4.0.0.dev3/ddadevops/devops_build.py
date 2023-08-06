import deprecation
from subprocess import run, CalledProcessError
from .domain import Devops
from .infrastructure import ProjectRepository, FileApi


@deprecation.deprecated(deprecated_in="3.2", details="create objects direct instead")
def create_devops_build_config(
    stage, project_root_path, module, build_dir_name="target"
):
    return {
        "stage": stage,
        "project_root_path": project_root_path,
        "module": module,
        "build_dir_name": build_dir_name,
    }

def get_devops_build(project):
    return project.get_property("devops_build")


@deprecation.deprecated(deprecated_in="3.2")
# TODO: Remove from here!
def get_tag_from_latest_commit():
    try:
        value = run(
            "git describe --abbrev=0 --tags --exact-match",
            shell=True,
            capture_output=True,
            check=True,
        )
        return value.stdout.decode("UTF-8").rstrip()
    except CalledProcessError:
        return None


class DevopsBuild:
    def __init__(self, project, config: map = None, devops: Devops = None):
        self.project = project
        self.file_api = FileApi()
        self.repo = ProjectRepository()
        if not devops:
            devops = Devops(
                stage=config["stage"],
                project_root_path=config["project_root_path"],
                module=config["module"],
                name=project.name,
                build_dir_name=config["build_dir_name"],
            )
        self.repo.set_devops(self.project, devops)
        self.repo.set_build(self.project, self)

    def name(self):
        devops = self.repo.get_devops(self.project)
        return devops.name

    def build_path(self):
        devops = self.repo.get_devops(self.project)
        return devops.build_path()

    def initialize_build_dir(self):
        devops = self.repo.get_devops(self.project)
        self.file_api.clean_dir(devops.build_path())
