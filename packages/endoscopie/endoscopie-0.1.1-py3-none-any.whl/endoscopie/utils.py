import json
import math
import os
import subprocess
import yaml

from endoscopie.logarithm import Logarithm
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from time import sleep
from typing import Optional

logger = Logarithm(__name__)


class CommandException(Exception):
    def __init__(self, error_message, return_code, stdout, stderr):
        self.error_message = error_message
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return f"{self.error_message} [return_code: {self.return_code}]"


def execute_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
    except Exception as e:
        logger.error(e)

    if process.returncode >= 1:
        logger.error(err.decode())
        raise CommandException(f"Command Execution Failed!", process.returncode, out.decode(), err.decode())

    return out.decode(), err.decode()


def render_terraform_template(tf_path, tf_file, metadata):
    env = Environment(loader=FileSystemLoader(tf_path))
    temp_tf = env.get_template(tf_file)
    terraform_tf = temp_tf.render(metadata)

    with open(f"{tf_path}/openstack-vm.tf", "w") as file:
        file.write(terraform_tf)


def get_metadata(meta_file):
    with open(meta_file) as mf:
        metadata = json.load(mf)
    return metadata


def get_server_info(template_dir, yaml_data):
    raw_data = get_resources(template_dir)

    servers = []
    resources = raw_data.get('values').get('root_module').get('resources')

    for resource in resources:
        flavor_id = resource.get('values').get('flavor_id')
        idx = int(resource.get('name').split('-')[-1]) - 1
        assert_that = yaml_data['images'][idx]['assertThat']

        sequence = 0
        for i, flavor in enumerate(yaml_data['images'][idx]['flavors']):
            if flavor_id != flavor['id']:
                continue
            sequence = i

        server = {
            "id": resource.get('values').get("id"),
            "name": resource.get('name'),
            "access_ip_v4": resource.get('values').get('access_ip_v4'),
            "access_ip_v6": resource.get('values').get('access_ip_v6'),
            "floating_ip": resource.get('values').get('floating_ip'),
            "keypair": yaml_data["instance"]["keypair"]["path"],
            "assertThat": {
                "resources": assert_that["resources"][sequence],
                "processes": assert_that["processes"],
                "ports": assert_that["ports"]
            }
        }

        servers.append(server)

    o = {
        "bastionHost": yaml_data["bastionHost"],
        "servers": servers
    }
    logger.debug(o)

    return o


def get_resources(template_dir) -> str:
    cmd = f"""
    bash -c "
    cd {template_dir}
    terraform show -json terraform.tfstate | jq
    " 
    """

    out, err = execute_command(cmd)

    return json.loads(out.strip())


def check_file_exist(file: Optional[Path]) -> tuple:
    error = None
    output = None

    if not file.exists():
        error = f":boom: [bold red]No such file or directory.[/bold red]"

        return output, error
    else:
        if file.is_file():
            if file.suffix not in ['.yaml', '.yml']:
                error = f":boom: [bold red] {file.absolute()}[/bold red] is not a [bold]YAML[/bold] file."
            # else:
            #     output = f":white_check_mark: [bold green] {file.absolute()}[/bold green]"
        elif file.is_dir():
            error = f":boom: [bold red]{file}[/bold red] is a directory."
        elif file.is_symlink():
            error = f":boom: [bold red]{file}[/bold red] is a symbolic link."
        elif file.is_mount():
            error = f":boom: [bold red]{file}[/bold red] is a POSIX mount point."
        elif file.is_block_device():
            error = f":boom: [bold red]{file}[/bold red] is a block device."
        elif file.is_char_device():
            error = f":boom: [bold red]{file}[/bold red] is a character device."
        elif file.is_socket():
            error = f":boom: [bold red]{file}[/bold red] is a socket."
        else:
            error = f":boom: [bold red]{file}[/bold red] is "

    return output, error


def unset_variables() -> None:
    cmd = f"""
    bash -c "
    unset OS_REGION_NAME
    unset OS_AUTH_URL
    unset OS_AUTH_TYPE
    unset OS_APPLICATION_CREDENTIAL_ID
    unset OS_APPLICATION_CREDENTIAL_SECRET
    "
    """

    out, err = execute_command(cmd)
    if err:
        logger.error(err.strip())

    logger.debug(out.strip())

    return None


def load_yaml_file(target: Optional[Path]) -> dict:
    logger.debug("Loading YAML file...")

    yml = {}
    try:
        with open(target, 'r') as file:
            yml = yaml.load(file, Loader=yaml.FullLoader)
    except IOError as ioe:
        logger.error(f"Loading the YAML file failed. - {ioe}")

    return yml


def _check_openstack_credential(openstack: dict) -> bool:
    malformed = False

    if 'openstack' in openstack.keys():
        malformed = True

    return malformed


def setenv(openstack: dict) -> None:
    logger.info("Setting environment variables...")

    os.environ['OS_REGION_NAME'] = openstack.get('OS_REGION_NAME')
    os.environ['OS_AUTH_URL'] = openstack.get('OS_AUTH_URL')
    os.environ['OS_AUTH_TYPE'] = openstack.get('OS_AUTH_TYPE')
    os.environ['OS_APPLICATION_CREDENTIAL_ID'] = openstack.get('OS_APPLICATION_CREDENTIAL_ID')
    os.environ['OS_APPLICATION_CREDENTIAL_SECRET'] = openstack.get('OS_APPLICATION_CREDENTIAL_SECRET')

    logger.debug(f"OS_REGION_NAME={os.getenv('OS_REGION_NAME')}")
    logger.debug(f"OS_AUTH_URL={os.getenv('OS_AUTH_URL')}")
    logger.debug(f"OS_AUTH_TYPE={os.getenv('OS_AUTH_TYPE')}")
    logger.debug(f"OS_APPLICATION_CREDENTIAL_ID={os.getenv('OS_APPLICATION_CREDENTIAL_ID')}")
    logger.debug(f"OS_APPLICATION_CREDENTIAL_SECRET={os.getenv('OS_APPLICATION_CREDENTIAL_SECRET')}")


def retry(cnt: int) -> int:
    sleep(3)
    var = cnt + 1
    return var


def gib(size: int) -> int:
    return int(size / math.pow(1024, 3))


def description(version):
    logo = f"""


$$$$$$$$\                 $$\                                                   $$\           
$$  _____|                $$ |                                                  \__|          
$$ |      $$$$$$$\   $$$$$$$ | $$$$$$\   $$$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$\  $$\  $$$$$$\  
$$$$$\    $$  __$$\ $$  __$$ |$$  __$$\ $$  _____|$$  _____|$$  __$$\ $$  __$$\ $$ |$$  __$$\ 
$$  __|   $$ |  $$ |$$ /  $$ |$$ /  $$ |\$$$$$$\  $$ /      $$ /  $$ |$$ /  $$ |$$ |$$$$$$$$ |
$$ |      $$ |  $$ |$$ |  $$ |$$ |  $$ | \____$$\ $$ |      $$ |  $$ |$$ |  $$ |$$ |$$   ____|
$$$$$$$$\ $$ |  $$ |\$$$$$$$ |\$$$$$$  |$$$$$$$  |\$$$$$$$\ \$$$$$$  |$$$$$$$  |$$ |\$$$$$$$\ 
\________|\__|  \__| \_______| \______/ \_______/  \_______| \______/ $$  ____/ \__| \_______|
                                                                      $$ |                    
                                                                      $$ |                    
                                                                      \__|                    

                                                                            Version {version}
"""
    return logo


def mklogdir():
    app_path = f"{str(Path.home())}/.endoscopie"
    os.makedirs(app_path, exist_ok=True)
