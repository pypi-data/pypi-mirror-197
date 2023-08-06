from pathlib import Path
from sys import stdout
from pkg_resources import resource_string
from os import chmod
import yaml
from .domain import Devops, Docker, C4k
from .python_util import execute


class ProjectRepository:
    def get_devops(self, project) -> Devops:
        return project.get_property("build")

    def set_devops(self, project, build: Devops):
        project.set_property("build", build)

    def  get_docker(self, project) -> Docker:
        return project.get_property("docker_build")

    def  set_docker(self, project, build: Docker):
        project.set_property("docker_build", build)

    def get_c4k(self, project) -> C4k:
        return project.get_property("c4k_build")

    def set_c4k(self, project, build: C4k):
        project.set_property("c4k_build", build)


class ResourceApi:
    def read_resource(self, path: str) -> bytes:
        return resource_string(__name__, path)


class FileApi:
    def clean_dir(self, directory: str):
        execute("rm -rf " + directory, shell=True)
        execute("mkdir -p " + directory, shell=True)

    def cp_force(self, src: str, target_dir: str):
        execute("cp -f " + src + "* " + target_dir, shell=True)

    def cp_recursive(self, src: str, target_dir: str):
        execute("cp -r " + src + " " + target_dir, shell=True)

    def write_data_to_file(self, path: Path, data: bytes):
        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(data.decode(stdout.encoding))

    def write_yaml_to_file(self, path: Path, data: map):
        with open(path, "w", encoding="utf-8") as output_file:
            yaml.dump(data, output_file)
        chmod(path, 0o600)


class DockerApi:
    def image(self, name: str, path: Path):
        execute(
            "docker build -t "
            + name
            + " --file "
            + path
            + "/image/Dockerfile "
            + path
            + "/image",
            shell=True,
        )

    def drun(self, name: str):
        execute('docker run -it --entrypoint="" ' + name + " /bin/bash", shell=True)

    def dockerhub_login(self, username: str, password: str):
        execute(
            "docker login --username " + username + " --password " + password,
            shell=True,
        )

    def dockerhub_publish(self, name: str, username: str, tag=None):
        if tag is not None:
            execute(
                "docker tag " + name + " " + username + "/" + name + ":" + tag,
                shell=True,
            )
            execute("docker push " + username + "/" + name + ":" + tag, shell=True)
        execute(
            "docker tag " + name + " " + username + "/" + name + ":latest", shell=True
        )
        execute("docker push " + username + "/" + name + ":latest", shell=True)

    def test(self, name: str, path: Path):
        execute(
            "docker build -t "
            + name
            + "-test "
            + "--file "
            + path
            + "/test/Dockerfile "
            + path
            + "/test",
            shell=True,
        )


class ExecutionApi:
    def execute(command: str, dry_run=False):
        output = ""
        if dry_run:
            print(command)
        else:
            output = execute(command, True)
            print(output)
        return output
