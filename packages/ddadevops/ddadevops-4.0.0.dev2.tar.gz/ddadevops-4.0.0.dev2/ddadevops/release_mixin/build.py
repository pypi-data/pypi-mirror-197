import sys
import os
from pathlib import Path
from ddadevops import *

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# adding the current directory to
# the sys.path.
sys.path.append(current)
 
# now we can import the module in the current
# directory.

from pybuilder.core import task, init
from ddadevops import *
from release_mixin import ReleaseMixin, create_release_mixin_config

CONFIG_FILE = Path('config.json')
MAIN_BRANCH = 'main'
STAGE = 'test'
PROJECT_ROOT_PATH = '.'
MODULE = 'test'
BUILD_DIR_NAME = "build_dir"

class MyBuild(ReleaseMixin):
    pass

@init
def initialize(project):
    project.build_depends_on('ddadevops>=3.1.2')
    config = create_release_mixin_config(CONFIG_FILE, MAIN_BRANCH)
    config.update({'stage': STAGE,
                   'module': MODULE,
                   'project_root_path': PROJECT_ROOT_PATH,
                   'build_dir_name': BUILD_DIR_NAME})
    build = MyBuild(project, config)
    build.initialize_build_dir()

@task
def release(project):
    build = get_devops_build(project)

    build.prepare_release()
    build.tag_and_push_release()
