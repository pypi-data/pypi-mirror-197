import sys
from os import chmod
from json import load, dumps
from subprocess import run
from packaging import version
from pkg_resources import resource_string
from dda_python_terraform import Terraform, IsFlagged
from .python_util import filter_none
from .devops_build import DevopsBuild, create_devops_build_config




def create_devops_terraform_build_config(stage,
                                         project_root_path,
                                         module,
                                         additional_vars,
                                         build_dir_name='target',
                                         output_json_name=None,
                                         use_workspace=True,
                                         use_package_common_files=True,
                                         build_commons_path=None,
                                         terraform_build_commons_dir_name='terraform',
                                         debug_print_terraform_command=False,
                                         additional_tfvar_files=None,
                                         terraform_semantic_version="1.0.8"):
    if not output_json_name:
        output_json_name = 'out_' + module + '.json'
    if not additional_tfvar_files:
        additional_tfvar_files = []
    ret = create_devops_build_config(
        stage, project_root_path, module, build_dir_name)
    ret.update({'additional_vars': additional_vars,
                'output_json_name': output_json_name,
                'use_workspace': use_workspace,
                'use_package_common_files': use_package_common_files,
                'build_commons_path': build_commons_path,
                'terraform_build_commons_dir_name': terraform_build_commons_dir_name,
                'debug_print_terraform_command': debug_print_terraform_command,
                'additional_tfvar_files': additional_tfvar_files,
                'terraform_semantic_version': terraform_semantic_version})
    return ret

class DevopsTerraformBuild(DevopsBuild):

    def __init__(self, project, config):
        super().__init__(project, config)
        project.build_depends_on('dda-python-terraform')
        self.additional_vars = config['additional_vars']
        self.output_json_name = config['output_json_name']
        self.use_workspace = config['use_workspace']
        self.use_package_common_files = config['use_package_common_files']
        self.build_commons_path = config['build_commons_path']
        self.terraform_build_commons_dir_name = config['terraform_build_commons_dir_name']
        self.debug_print_terraform_command = config['debug_print_terraform_command']
        self.additional_tfvar_files = config['additional_tfvar_files']
        self.terraform_semantic_version = config['terraform_semantic_version']

    def terraform_build_commons_path(self):
        mylist = [self.build_commons_path,
                  self.terraform_build_commons_dir_name]
        return '/'.join(filter_none(mylist)) + '/'

    def project_vars(self):
        ret = {'stage': self.stage}
        if self.module:
            ret['module'] = self.module
        if self.additional_vars:
            ret.update(self.additional_vars)
        return ret

    def copy_build_resource_file_from_package(self, name):
        my_data = resource_string(
            __name__, "src/main/resources/terraform/" + name)
        with open(self.build_path() + '/' + name, "w", encoding="utf-8") as output_file:
            output_file.write(my_data.decode(sys.stdout.encoding))

    def copy_build_resources_from_package(self):
        self.copy_build_resource_file_from_package('versions.tf')
        self.copy_build_resource_file_from_package('terraform_build_vars.tf')

    def copy_build_resources_from_dir(self):
        run('cp -f ' + self.terraform_build_commons_path() +
            '* ' + self.build_path(), shell=False, check=False)

    def copy_local_state(self):
        run('cp terraform.tfstate '  + self.build_path(), shell=False, check=False)

    def rescue_local_state(self):
        run('cp ' + self.build_path() + '/terraform.tfstate .', shell=False, check=False)

    def initialize_build_dir(self):
        super().initialize_build_dir()
        if self.use_package_common_files:
            self.copy_build_resources_from_package()
        else:
            self.copy_build_resources_from_dir()
        self.copy_local_state()
        run('cp *.tf ' + self.build_path(), shell=True, check=False)
        run('cp *.properties ' + self.build_path(), shell=True, check=False)
        run('cp *.tfvars ' + self.build_path(), shell=True, check=False)
        run('cp -r scripts ' + self.build_path(), shell=True, check=False)

    def post_build(self):
        self.rescue_local_state()

    def init_client(self):
        terraform = Terraform(working_dir=self.build_path(), terraform_semantic_version=self.terraform_semantic_version)
        terraform.init()
        self.print_terraform_command(terraform)
        if self.use_workspace:
            try:
                terraform.workspace('select', self.stage)
                self.print_terraform_command(terraform)
            except:
                terraform.workspace('new', self.stage)
                self.print_terraform_command(terraform)
        return terraform

    def write_output(self, terraform):
        result = terraform.output(json=IsFlagged)
        self.print_terraform_command(terraform)
        with open(self.build_path() + self.output_json_name, "w", encoding="utf-8") as output_file:
            output_file.write(dumps(result))
        chmod(self.build_path() + self.output_json_name, 0o600)

    def read_output_json(self):
        with open(self.build_path() + self.output_json_name, 'r', encoding="utf-8") as file:
            return load(file)

    def plan(self):
        terraform = self.init_client()
        return_code, _, stderr = terraform.plan(detailed_exitcode=None, capture_output=False, raise_on_error=False,
                var=self.project_vars(),
                var_file=self.additional_tfvar_files)
        self.post_build()
        self.print_terraform_command(terraform)
        if return_code > 0:
            raise Exception(return_code, "terraform error:", stderr)

    def plan_fail_on_diff(self):
        terraform = self.init_client()
        return_code, _, stderr = terraform.plan(detailed_exitcode=IsFlagged, capture_output=False, raise_on_error=False,
                var=self.project_vars(),
                var_file=self.additional_tfvar_files)
        self.post_build()
        self.print_terraform_command(terraform)
        if return_code not in (0, 2):
            raise Exception(return_code, "terraform error:", stderr)
        if return_code == 2:
            raise Exception(return_code, "diff in config found:", stderr)

    def apply(self, auto_approve=False):
        terraform = self.init_client()
        if auto_approve:
            auto_approve_flag = IsFlagged
        else:
            auto_approve_flag = None
        if version.parse(self.terraform_semantic_version) >= version.parse("1.0.0"):
            return_code, _, stderr = terraform.apply(capture_output=False, raise_on_error=True,
                    auto_approve=auto_approve_flag,
                    var=self.project_vars(),
                    var_file=self.additional_tfvar_files)
        else:
            return_code, _, stderr = terraform.apply(capture_output=False, raise_on_error=True,
                    skip_plan=auto_approve,
                    var=self.project_vars(),
                    var_file=self.additional_tfvar_files)
        self.write_output(terraform)
        self.post_build()
        self.print_terraform_command(terraform)
        if return_code > 0:
            raise Exception(return_code, "terraform error:", stderr)

    def refresh(self):
        terraform = self.init_client()
        return_code, _, stderr = terraform.refresh(
                var=self.project_vars(),
                var_file=self.additional_tfvar_files)
        self.write_output(terraform)
        self.post_build()
        self.print_terraform_command(terraform)
        if return_code > 0:
            raise Exception(return_code, "terraform error:", stderr)

    def destroy(self, auto_approve=False):
        terraform = self.init_client()
        if auto_approve:
            auto_approve_flag = IsFlagged
        else:
            auto_approve_flag = None
        if version.parse(self.terraform_semantic_version) >= version.parse("1.0.0"):
            return_code, _, stderr = terraform.destroy(capture_output=False, raise_on_error=True,
                    auto_approve=auto_approve_flag,
                    var=self.project_vars(),
                    var_file=self.additional_tfvar_files)
        else:
            return_code, _, stderr = terraform.destroy(capture_output=False, raise_on_error=True,
                    force=auto_approve_flag,
                    var=self.project_vars(),
                    var_file=self.additional_tfvar_files)
        self.post_build()
        self.print_terraform_command(terraform)
        if return_code > 0:
            raise Exception(return_code, "terraform error:", stderr)

    def tf_import(self, tf_import_name, tf_import_resource,):
        terraform = self.init_client()
        return_code, _, stderr = terraform.import_cmd(tf_import_name, tf_import_resource,
                      capture_output=False, raise_on_error=True,
                      var=self.project_vars(),
                      var_file=self.additional_tfvar_files)
        self.post_build()
        self.print_terraform_command(terraform)
        if return_code > 0:
            raise Exception(return_code, "terraform error:", stderr)

    def print_terraform_command(self, terraform):
        if self.debug_print_terraform_command:
            output = 'cd ' + self.build_path() + ' && ' + terraform.latest_cmd()
            print(output)
