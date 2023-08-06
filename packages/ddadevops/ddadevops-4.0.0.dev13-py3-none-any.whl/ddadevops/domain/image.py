from .common import (
    filter_none,
    Validateable,
    Devops,
)

class Image(Validateable):
    def __init__(
        self,
        dockerhub_user,
        dockerhub_password,
        devops: Devops,
        build_dir_name="target",
        use_package_common_files=True,
        build_commons_path=None,
        docker_build_commons_dir_name="docker",
        docker_publish_tag=None,
    ):
        self.dockerhub_user = dockerhub_user
        self.dockerhub_password = dockerhub_password
        self.use_package_common_files = use_package_common_files
        self.build_commons_path = build_commons_path
        self.docker_build_commons_dir_name = docker_build_commons_dir_name
        self.docker_publish_tag = docker_publish_tag
        self.devops = devops

    def docker_build_commons_path(self):
        list = [self.build_commons_path, self.docker_build_commons_dir_name]
        return "/".join(filter_none(list)) + "/"
