import deprecation
from .domain import Image
from .application import ImageBuildService
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


class DevopsImageBuild(DevopsBuild):
    def __init__(self, project, config: map = None, image: Image = None):
        self.image_build_service = ImageBuildService()
        if not image:
            image = Image(
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
        self.repo.set_docker(self.project, image)

    def initialize_build_dir(self):
        super().initialize_build_dir()
        image = self.repo.get_docker(self.project)
        self.image_build_service.initialize_build_dir(image)

    def image(self):
        image = self.repo.get_docker(self.project)
        self.image_build_service.image(image)

    def drun(self):
        image = self.repo.get_docker(self.project)
        self.image_build_service.drun(image)

    def dockerhub_login(self):
        image = self.repo.get_docker(self.project)
        self.image_build_service.dockerhub_login(image)

    def dockerhub_publish(self):
        image = self.repo.get_docker(self.project)
        self.image_build_service.dockerhub_publish(image)

    def test(self):
        image = self.repo.get_docker(self.project)
        self.image_build_service.test(image)
