from string import Template
import deprecation
from .python_util import execute_live
from .devops_build import DevopsBuild


CONFIG_BASE = """
fqdn: $fqdn
"""
CONFIG_IPV4 = """node:
  ipv4: $ipv4
"""
CONFIG_IPV6 = """  ipv6: $ipv6
"""
CONFIG_CERTMANAGER = """certmanager:
  email: $letsencrypt_email
  letsencryptEndpoint: $letsencrypt_endpoint
"""
CONFIG_ECHO = """echo: $echo
"""


def add_provs_k3s_mixin_config(config,
                               provision_user='root',
                               echo=None,
                               k3s_config_template=None,
                               letsencrypt_email=None,
                               letsencrypt_endpoint=None,
                               fqdn=None,
                               ipv4=None,
                               ipv6=None,
                               app_filename_to_provision=None):
    template_text = k3s_config_template
    if template_text is None:
        template_text = CONFIG_BASE
        if letsencrypt_endpoint is not None:
            template_text += CONFIG_CERTMANAGER
        if echo is not None:
            template_text += CONFIG_ECHO
        if ipv4  is not None:
            template_text += CONFIG_IPV4
        if ipv6  is not None:
            template_text += CONFIG_IPV6

    config.update({'ProvsK3sMixin':
                   {'fqdn': fqdn,
                    'provision_user': provision_user,
                    'ipv4': ipv4,
                    'ipv6': ipv6,
                    'letsencrypt_email': letsencrypt_email,
                    'letsencrypt_endpoint': letsencrypt_endpoint,
                    'echo': echo,
                    'k3s_config_template': template_text,
                    'app_filename_to_provision': app_filename_to_provision}})
    return config


class ProvsK3sMixin(DevopsBuild):

    def __init__(self, project, config):
        super().__init__(project, config)
        provs_k3s_mixin_config = config['ProvsK3sMixin']
        self.fqdn = provs_k3s_mixin_config['fqdn']
        self.put('fqdn', self.fqdn)
        self.provision_user = provs_k3s_mixin_config['provision_user']
        self.put('provision_user', self.provision_user)
        self.ipv4 = provs_k3s_mixin_config['ipv4']
        self.put('ipv4', self.ipv4)
        self.ipv6 = provs_k3s_mixin_config['ipv6']
        self.put('ipv6', self.ipv6)
        self.letsencrypt_email = provs_k3s_mixin_config['letsencrypt_email']
        self.put('letsencrypt_email', self.letsencrypt_email)
        self.letsencrypt_endpoint = provs_k3s_mixin_config['letsencrypt_endpoint']
        self.put('letsencrypt_endpoint', self.letsencrypt_endpoint)
        self.echo = provs_k3s_mixin_config['echo']
        self.put('echo', self.echo)
        self.k3s_config_template_text = provs_k3s_mixin_config['k3s_config_template']
        self.k3s_config_template = Template(
            provs_k3s_mixin_config['k3s_config_template'])
        self.put('k3s_config_template', self.k3s_config_template)
        self.app_filename_to_provision = provs_k3s_mixin_config['app_filename_to_provision']
        self.put('app_filename_to_provision', self.app_filename_to_provision)

    def update_runtime_config(self, fqdn, ipv4, ipv6=None):
        self.fqdn = fqdn
        self.put('fqdn', fqdn)
        self.ipv4 = ipv4
        self.put('ipv4', ipv4)
        self.ipv6 = ipv6
        self.put('ipv6', ipv6)
        template_text = self.k3s_config_template_text
        if ipv4  is not None:
            template_text += CONFIG_IPV4
        if ipv6  is not None:
            template_text += CONFIG_IPV6
        self.k3s_config_template_text = template_text
        self.put('k3s_config_template_text', template_text)
        template = Template(template_text)
        self.k3s_config_template = template
        self.put('k3s_config_template', template)

    def write_provs_config(self):
        substitutes = self.get_keys(['fqdn', 'ipv4', 'ipv6', 'letsencrypt_email',
                                     'letsencrypt_endpoint', 'echo'])
        with open(self.build_path() + '/out_k3sServerConfig.yaml', "w", encoding="utf-8") as output_file:
            output_file.write(self.k3s_config_template.substitute(substitutes))

    @deprecation.deprecated(deprecated_in="3.1")
    def provs_server(self, dry_run=False):
        self.provs_apply(dry_run)

    def provs_apply(self, dry_run=False):
        cmd = ['provs-server.jar', 'k3s', self.provision_user + '@' + self.fqdn, '-c',
               self.build_path() + '/out_k3sServerConfig.yaml',
               '-a', self.build_path() + '/' + self.app_filename_to_provision]
        if dry_run:
            print(" ".join(cmd))
        else:
            execute_live(cmd)
