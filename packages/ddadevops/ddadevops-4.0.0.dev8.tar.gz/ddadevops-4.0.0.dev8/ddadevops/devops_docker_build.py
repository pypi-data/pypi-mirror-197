import deprecation
from .domain import Docker
from .application import DockerBuildService
from .devops_build import DevopsBuild, create_devops_build_config


@deprecation.deprecated(deprecated_in="3.2", details="create objects direct instead")
def create_devops_docker_build_config(
    stage,
    project_root_path,
    module,
    dockerhub_user,
    dockerhub_password,
    build_dir_name="target",
    use_package_common_files=True,
    build_commons_path=None,
    docker_build_commons_dir_name="docker",
    docker_publish_tag=None,
):
    ret = create_devops_build_config(stage, project_root_path, module, build_dir_name)
    ret.update(
        {
            "dockerhub_user": dockerhub_user,
            "dockerhub_password": dockerhub_password,
            "use_package_common_files": use_package_common_files,
            "docker_build_commons_dir_name": docker_build_commons_dir_name,
            "build_commons_path": build_commons_path,
            "docker_publish_tag": docker_publish_tag,
        }
    )
    return ret


class DevopsDockerBuild(DevopsBuild):
    def __init__(self, project, config: map = None, docker: Docker = None):
        self.docker_build_service = DockerBuildService()
        if not docker:
            docker = Docker(
                dockerhub_user=config["dockerhub_user"],
                dockerhub_password=config["dockerhub_password"],
                use_package_common_files=config["use_package_common_files"],
                build_commons_path=config["build_commons_path"],
                docker_build_commons_dir_name=config["docker_build_commons_dir_name"],
                docker_publish_tag=config["docker_publish_tag"],
            )
            super().__init__(project, config=config)
        else:
            super().__init__(project, devops=docker.devops)
        self.repo.set_docker(self.project, docker)

    def initialize_build_dir(self):
        super().initialize_build_dir()
        docker = self.repo.get_docker(self.project)
        self.docker_build_service.initialize_build_dir(docker)

    def image(self):
        docker = self.repo.get_docker(self.project)
        self.docker_build_service.image(docker)

    def drun(self):
        docker = self.repo.get_docker(self.project)
        self.docker_build_service.drun(docker)

    def dockerhub_login(self):
        docker = self.repo.get_docker(self.project)
        self.docker_build_service.dockerhub_login(docker)

    def dockerhub_publish(self):
        docker = self.repo.get_docker(self.project)
        self.docker_build_service.dockerhub_publish(docker)

    def test(self):
        docker = self.repo.get_docker(self.project)
        self.test.dockerhub_publish(docker)
