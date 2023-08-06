from endoscopie import utils
from endoscopie.logarithm import Logarithm

logger = Logarithm(__name__)


def create(template_dir):
    cmd_create = f"""
    bash -c "
    cd {template_dir}
    terraform init
    terraform plan
    terraform apply -auto-approve
    "
    """
    logger.info("Terraform will be created resources..")
    out, err = utils.execute_command(cmd_create)

    if err:
        logger.error(err)

    logger.debug(out)

    return out, err


def delete(template_dir):
    cmd_delete = f"""
    bash -c "
    cd {template_dir}
    pwd
    terraform init
    terraform plan
    terraform apply -destroy -auto-approve
    "
    """

    server_list(template_dir)
    logger.info("Terraform will be deleted resources..")
    out, err = utils.execute_command(cmd_delete)

    if err:
        logger.error(err)

    logger.debug(out)

    return out, err


def server_list(template_dir):
    cmd = f"""
    bash -c "
    cd {template_dir}
    terraform state list
    "
    """

    out, err = utils.execute_command(cmd)
    vm_server_list = out.strip().split("\n")

    # logger.debug(f"Server list : {vm_server_list}")

    return vm_server_list


def is_exist(template_dir):

    logger.debug(f"Terraform template path: {template_dir}")

    instances = server_list(template_dir)
    vm_server_list = [x for x in instances if x != '']

    if len(vm_server_list) <= 0:
        return False

    return True
