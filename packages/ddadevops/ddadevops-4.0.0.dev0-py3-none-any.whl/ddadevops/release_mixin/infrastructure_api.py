import json
import re
import subprocess as sub
from abc import ABC, abstractmethod
from pathlib import Path


class FileHandler(ABC):

    @classmethod
    def from_file_path(cls, file_path):
        config_file_type = file_path.suffix
        match config_file_type:
            case '.json':
                file_handler = JsonFileHandler()
            case '.gradle':
                file_handler = GradleFileHandler()
            case '.clj':
                file_handler = ClojureFileHandler()
            case '.py':
                file_handler = PythonFileHandler()
            case _:
                raise Exception(
                    f'The file type "{config_file_type}" is not implemented')

        file_handler.config_file_path = file_path
        file_handler.config_file_type = config_file_type
        return file_handler

    @abstractmethod
    def parse(self) -> tuple[list[int], bool]:
        pass

    @abstractmethod
    def write(self, version_string):
        pass


class JsonFileHandler(FileHandler):

    def parse(self) -> tuple[list[int], bool]:
        with open(self.config_file_path, 'r') as json_file:
            json_version = json.load(json_file)['version']
            is_snapshot = False
            if '-SNAPSHOT' in json_version:
                is_snapshot = True
                json_version = json_version.replace('-SNAPSHOT', '')
            version = [int(x) for x in json_version.split('.')]
            return version, is_snapshot

    def write(self, version_string):
        with open(self.config_file_path, 'r+') as json_file:
            json_data = json.load(json_file)
            json_data['version'] = version_string
            json_file.seek(0)
            json.dump(json_data, json_file, indent=4)
            json_file.truncate()


class GradleFileHandler(FileHandler):

    def parse(self) -> tuple[list[int], bool]:
        with open(self.config_file_path, 'r') as gradle_file:
            contents = gradle_file.read()
            version_line = re.search("\nversion = .*", contents)
            exception = Exception("Version not found in gradle file")
            if version_line is None:
                raise exception

            version_line = version_line.group()
            version_string = re.search(
                '[0-9]*\\.[0-9]*\\.[0-9]*(-SNAPSHOT)?', version_line)
            if version_string is None:
                raise exception

            version_string = version_string.group()
            is_snapshot = False
            if '-SNAPSHOT' in version_string:
                is_snapshot = True
                version_string = version_string.replace('-SNAPSHOT', '')

            version = [int(x) for x in version_string.split('.')]

            return version, is_snapshot

    def write(self, version_string):
        with open(self.config_file_path, 'r+') as gradle_file:
            contents = gradle_file.read()
            version_substitute = re.sub(
                '\nversion = "[0-9]*\\.[0-9]*\\.[0-9]*(-SNAPSHOT)?"', f'\nversion = "{version_string}"', contents)
            gradle_file.seek(0)
            gradle_file.write(version_substitute)
            gradle_file.truncate()


class PythonFileHandler(FileHandler):

    def parse(self) -> tuple[list[int], bool]:
        with open(self.config_file_path, 'r') as python_file:
            contents = python_file.read()
            version_line = re.search("\nversion = .*\n", contents)
            exception = Exception("Version not found in gradle file")
            if version_line is None:
                raise exception

            version_line = version_line.group()
            version_string = re.search(
                '[0-9]*\\.[0-9]*\\.[0-9]*(-SNAPSHOT)?', version_line)
            if version_string is None:
                raise exception

            version_string = version_string.group()
            is_snapshot = False
            if '-SNAPSHOT' in version_string:
                is_snapshot = True
                version_string = version_string.replace('-SNAPSHOT', '')

            version = [int(x) for x in version_string.split('.')]

            return version, is_snapshot

    def write(self, version_string):
        with open(self.config_file_path, 'r+') as python_file:
            contents = python_file.read()
            version_substitute = re.sub(
                '\nversion = "[0-9]*\\.[0-9]*\\.[0-9]*(-SNAPSHOT)?"', f'\nversion = "{version_string}"', contents)
            python_file.seek(0)
            python_file.write(version_substitute)
            python_file.truncate()


class ClojureFileHandler(FileHandler):

    def parse(self) -> tuple[list[int], bool]:
        with open(self.config_file_path, 'r') as clj_file:
            contents = clj_file.read()
            version_line = re.search("^\\(defproject .*\n", contents)
            exception = Exception("Version not found in clj file")
            if version_line is None:
                raise exception

            version_line = version_line.group()
            version_string = re.search(
                '[0-9]*\\.[0-9]*\\.[0-9]*(-SNAPSHOT)?', version_line)
            if version_string is None:
                raise exception

            version_string = version_string.group()
            is_snapshot = False
            if '-SNAPSHOT' in version_string:
                is_snapshot = True
                version_string = version_string.replace('-SNAPSHOT', '')

            version = [int(x) for x in version_string.split('.')]

            return version, is_snapshot

    def write(self, version_string):
        with open(self.config_file_path, 'r+') as clj_file:
            clj_first = clj_file.readline()
            clj_rest = clj_file.read()
            version_substitute = re.sub(
                '[0-9]*\\.[0-9]*\\.[0-9]*(-SNAPSHOT)?', f'"{version_string}"\n', clj_first)
            clj_file.seek(0)
            clj_file.write(version_substitute)
            clj_file.write(clj_rest)
            clj_file.truncate()


class SystemAPI():

    def __init__(self):
        self.stdout = [""]
        self.stderr = [""]

    def run(self, args):
        stream = sub.Popen(args,
                           stdout=sub.PIPE,
                           stderr=sub.PIPE,
                           text=True,
                           encoding="UTF-8")
        self.stdout = stream.stdout.readlines()
        self.stderr = stream.stderr.readlines()

    def run_checked(self, *args):
        self.run(args)

        if len(self.stderr) > 0:
            raise Exception(f"Command failed with: {self.stderr}")


class GitApi():

    def __init__(self):
        self.system_api = SystemAPI()

    def get_latest_n_commits(self, n: int):
        self.system_api.run_checked(
            'git', 'log', '--oneline', '--format="%s %b"', f'-n {n}')
        return self.system_api.stdout

    def get_latest_commit(self):
        output = self.get_latest_n_commits(1)
        return " ".join(output)

    def tag_annotated(self, annotation: str, message: str, count: int):
        self.system_api.run_checked(
            'git', 'tag', '-a', annotation, '-m', message, f'HEAD~{count}')
        return self.system_api.stdout

    def get_latest_tag(self):
        self.system_api.run_checked('git', 'describe', '--tags', '--abbrev=0')
        return self.system_api.stdout

    def get_current_branch(self):
        self.system_api.run_checked('git', 'branch', '--show-current')
        return ''.join(self.system_api.stdout).rstrip()

    def init(self):
        self.system_api.run_checked('git', 'init')

    def add_file(self, file_path: Path):
        self.system_api.run_checked('git', 'add', file_path)
        return self.system_api.stdout

    def commit(self, commit_message: str):
        self.system_api.run_checked(
            'git', 'commit', '-m', commit_message)
        return self.system_api.stdout

    def push(self):
        self.system_api.run_checked('git', 'push')
        return self.system_api.stdout

    def checkout(self, branch: str):
        self.system_api.run_checked('git', 'checkout', branch)
        return self.system_api.stdout
