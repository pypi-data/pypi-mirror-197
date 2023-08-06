from .domain import Devops, Docker
from .infrastructure import FileApi, ResourceApi, DockerApi, ExecutionApi


class DockerBuildService:
    def __init__(self):
        self.file_api = FileApi()
        self.resource_api = ResourceApi()
        self.docker_api = DockerApi()

    def __copy_build_resource_file_from_package__(self, resource_name, docker: Docker):
        data = self.resource_api.read_resource(f"../../resources/docker/{resource_name}")
        self.file_api.write_data_to_file(
            f"{docker.devops.build_path()}/{resource_name}", data
        )

    def __copy_build_resources_from_package__(self, docker: Docker):
        self.__copy_build_resource_file_from_package__(
            "image/resources/install_functions.sh", docker
        )

    def __copy_build_resources_from_dir__(self, docker: Docker):
        self.file_api.cp_force(
            docker.docker_build_commons_path(), docker.devops.build_path()
        )

    def initialize_build_dir(self, docker: Docker):
        build_path = docker.devops.build_path()
        self.file_api.clean_dir(f"{build_path}/image/resources")
        if docker.use_package_common_files:
            self.__copy_build_resources_from_package__(docker)
        else:
            self.__copy_build_resources_from_dir__(docker)
        self.file_api.cp_recursive("image", build_path)
        self.file_api.cp_recursive("test", build_path)

    def image(self, docker: Docker):
        self.docker_api.image(docker.devops.name, docker.devops.build_path())

    def drun(self, docker: Devops):
        self.docker_api.drun(docker.devops.name)

    def dockerhub_login(self, docker: Docker):
        self.docker_api.dockerhub_login(
            docker.dockerhub_user, docker.dockerhub_password
        )

    def dockerhub_publish(self, docker: Docker):
        self.docker_api.dockerhub_publish(
            docker.devops.name, docker.dockerhub_user, docker.docker_publish_tag
        )

    def test(self, docker: Docker):
        self.docker_api.test(docker.devops.name, docker.devops.build_path())
