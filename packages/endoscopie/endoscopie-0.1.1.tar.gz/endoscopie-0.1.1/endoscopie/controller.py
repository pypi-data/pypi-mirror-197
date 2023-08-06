import logging
import os
import socket
import sys
import time
from enum import Enum

import typer
import yaml
from rich.table import Table

from endoscopie.ssh import EndoscopieSSHClient
from endoscopie.logarithm import Logarithm
from endoscopie import commando
from endoscopie import utils
from endoscopie import template_meta as meta
from endoscopie import terraform as tf_action

from paramiko.ssh_exception import ChannelException, BadHostKeyException, AuthenticationException, SSHException
from pathlib import Path
from rich import print as rprint
from rich import box
from rich.console import Console
from rich.panel import Panel

logger = Logarithm(__name__)
template_dir = Path(f"{os.path.dirname(os.path.abspath(__file__))}/templates")

# BACK1 = '\b'
LINE_UP = '\x1B[A'
# LINE_UP2 = '\x1B M'
LINE_CLEAR = '\x1B[2K'
GREEN = '\x1B[32m'

global results


class Result(Enum):
    PASSED = f"[bold green]PASSED[/bold green]"
    FAILED = f"[bold red]FAILED[/bold red]"


def provision(image_info: Path):
    logger.info("Initializing the backend...")
    with open(image_info) as file:
        images = yaml.load(file, Loader=yaml.FullLoader)

    tf_template_meta = meta.make(images)
    utils.render_terraform_template(template_dir, 'openstack-vm-tf.temp', tf_template_meta)

    logger.info("You may now begin working with Terraform.")
    out, err = tf_action.create(template_dir)

    if err.strip() != '':
        rprint(Panel(err.strip(), title="[bold red]Failed to create server(s).[/bold red] :boom:"))
        cleanup(True)

        raise typer.Abort()

    info = utils.get_server_info(template_dir, images)
    servers = info['servers']
    rprint(Panel('\n'.join([f" :computer: [bold green] \[{i['id']}][/bold green] {i['name']}" for i in servers]),
                    title="[green]Successfully created server(s).[/green]"))

    return info


def cleanup(destroy: bool):
    if destroy:
        tf_action.server_list(template_dir)
        logger.debug(template_dir)
        if tf_action.is_exist(os.path.abspath(template_dir)):
            out, err = tf_action.delete(template_dir)

            if err.strip() != '':
                rprint(
                    Panel.fit(err.strip(), title="[bold red]Failed to delete server(s).[/bold red] :boom:"))

                # @TODO 실패하면 인스턴스 삭제 제시도 추가
                raise typer.Abort()

            rprint(Panel(f" :ok: [bold green]Successfully deleted server(s).[/bold green]",
                        title="[green]Clean Up[/green]"))

        else:
            rprint(f"[red]The server(s) to clean up does not exist.[/red]")

    sys.exit(0)


def verify(target: dict):
    logger.info("Endoscopie will start verifying the server(s).")

    bastion_host = target['bastionHost']
    bastion_host_ip = bastion_host['ip']
    bastion_host_user = bastion_host['user']
    bastion_keypair_name = bastion_host['keypair']['name']
    bastion_keypair_path = bastion_host['keypair']['path']

    servers = target['servers']

    logging.getLogger("paramiko.transport").setLevel(logging.FATAL)

    # create ssh client to bastion host server
    bastion = EndoscopieSSHClient()
    bastion_pkey = bastion.get_key_object(bastion_keypair_path)
    bastion.connect(hostname=bastion_host_ip, username=bastion_host_user, keypair=bastion_pkey)

    bstin, bstout, bsterr = bastion.exec_command("hostname -I")
    bastion_private_ip = bstout.readline().strip().replace('\n', '')
    logger.debug(f"The bastion host's private ip: {bastion_private_ip}")

    bastion_transport = bastion.get_transport()
    source = (bastion_private_ip, 22)

    global results
    results = []

    for idx, server in enumerate(servers):
        private_ip = server['access_ip_v4']
        name = server['name']
        keypair_path = server['keypair']
        user = name.split('-')[1]

        destination = (private_ip, 22)

        instance = EndoscopieSSHClient()
        vm_pkey = instance.get_key_object(keypair_path)

        retry_cnt = 0
        retry_message = ""
        max = 60
        while retry_cnt < max:
            if retry_cnt > 0:
                retry_message = f"(Number of retries: {retry_cnt})"

            try:
                print(f"Connecting to {private_ip}:22 [{name}] ... {retry_message}")
                channel = bastion_transport.open_channel("direct-tcpip", destination, source, timeout=120)
                instance.connect(hostname=private_ip, username=user, keypair=vm_pkey, sock=channel)
                break
            except ChannelException as ce:
                logger.error(f"Connection failed. No route to host.")
                time.sleep(1)
                _upAndClear(1)
                retry_cnt = utils.retry(retry_cnt)
                continue
            except BadHostKeyException as bhke:
                logger.error(f"Connection failed. The server's host key could not be verified.")
                time.sleep(1)
                _upAndClear(1)
                retry_cnt = utils.retry(retry_cnt)
                continue
            except AuthenticationException as ae:
                logger.error(f"Connection failed. (Authentication failed)")
                time.sleep(1)
                _upAndClear(1)
                retry_cnt = utils.retry(retry_cnt)
                continue
            except SSHException as se:
                logger.error(f"Connection failed. There was any other error connecting or establishing an SSH session.")
                time.sleep(1)
                _upAndClear(1)
                retry_cnt = utils.retry(retry_cnt)
                continue
            except socket.error as ske:
                logger.error(f"Connection failed. Could not connect to {private_ip}:22.")
                time.sleep(1)
                _upAndClear(1)
                retry_cnt = utils.retry(retry_cnt)
                continue

        is_passed = f"[bold green]{Result.PASSED.value}[/bold green]"

        if retry_cnt >= max - 1:
            rprint(f">>>>> [{name} ({private_ip})] Connection failed. There was any other error connecting or establishing an SSH session.")
            rprint(f"[bold red]\[FAILED][/bold red] Abort assertions.")
            is_passed = Result.FAILED.value
            results.append([idx + 1, server['id'], name, private_ip, is_passed])
            continue

        print(f"{LINE_UP}Connecting to {private_ip}:22 [{name}] ... {retry_message} => {GREEN}Connected.")
        rprint(f">>>>>>>> Start assertion - \[{name} ({private_ip})]")
        stdin, stdout, stderr = instance.exec_command(commando.cmd['hostname_s'])
        actual_hostname = stdout.readline().replace('\n', '')
        expect_hostname = 'host-' + private_ip.replace('.', '-')

        if expect_hostname != actual_hostname:
            is_passed = Result.FAILED.value
            rprint(f"""[bold red]\[FAILED][/bold red] The hostname should be equal to the expected hostname.
    - Expect hostname : {expect_hostname}
    - Actual hostname : {actual_hostname}""")
        else:
            rprint(f"[bold green]\[PASSED][/bold green] The hostname is '{actual_hostname}'")

        stdin, stdout, stderr = instance.exec_command(commando.cmd['hostname_i'])
        actual_ip = stdout.readline().strip().replace('\n', '')

        if actual_ip != private_ip:
            is_passed = Result.FAILED.value
            rprint(f"""
            [bold red]\[FAILED][/bold red] The private ip(v4) should be equal to the expected private ip.
                   - Expect IP (v4) : {private_ip}
                   - Actual IP (v4) : {actual_ip} 
            """)
        else:
            rprint(f"[bold green]\[PASSED][/bold green] The private ip(v4) is {actual_ip}")

        stdin, stdout, stderr = instance.exec_command(commando.cmd['vCPU'])
        expect_cpu = int(server['assertThat']['resources']['vCPU'])
        actual_cpu = int(stdout.readline().replace('\n', ''))

        if actual_cpu != expect_cpu:
            is_passed = Result.FAILED.value
            rprint(f"""[bold red]\[FAILED][/bold red] Server's number of vCPU should be equal to the expect value.
    - Expect vCPU : {expect_cpu} 개
    - Actual vCPU : {actual_cpu} 개""")
        else:
            rprint(f"[bold green]\[PASSED][/bold green] Server's number of vCPU is {actual_cpu}")

        stdin, stdout, stderr = instance.exec_command(commando.cmd['memory'])
        expect_memory = int(server['assertThat']['resources']['memory'])
        actual_memory = int(stdout.readline().replace('\n', ''))

        if actual_memory != expect_memory:
            is_passed = Result.FAILED.value
            rprint(f"""[bold red]\[FAILED][/bold red] Server's maximum capacity of memory should be equal to the expect value.
    - Expect maximum capacity of memory : {expect_memory} GiB
    - Actual maximum capacity of memory : {actual_memory} GiB""")
        else:
            rprint(f"[bold green]\[PASSED][/bold green] Server's maximum capacity of memory is {actual_memory} GiB")

        stdin, stdout, stderr = instance.exec_command(commando.cmd['disk'])
        expect_disk_size = server['assertThat']['resources']['volume']
        actual_disk_size = int(stdout.readline().replace('\n', ''))

        if _gib(actual_disk_size) != expect_disk_size:
            is_passed = Result.FAILED.value
            rprint(f"""[bold red]\[FAILED][/bold red] Server's volume(/dev/vda) size should be equal to the expect value.
    - Expect volume size : {expect_disk_size} GiB
    - Actual volume size : {_gib(actual_disk_size)} GiB""")
        else:
            rprint(f"[bold green]\[PASSED][/bold green] Server's volume(/dev/vda) size is {_gib(actual_disk_size)} GiB")

        stdin, stdout, stderr = instance.exec_command(commando.cmd['outbound'])
        actual_egress = stdout.readline().replace('\n', '').strip()

        if actual_egress == '000':
            is_passed = Result.FAILED.value
            rprint(f"""
            [bold red]\[FAILED][/bold red] Server's egress status should be equal to the expect value.
                   - Expect egress : Connection to Google(https://google.com) was successful.
                   - Actual egress : Failed to connect to Google(https://google.com).
            """)
        else:
            rprint(f"[bold green]\[PASSED][/bold green] Connection to Google(https://google.com) was successful")

        processes = server['assertThat']['processes']
        for process in processes:
            stdin, stdout, stderr = instance.exec_command(commando.cmd['process'].format(process))
            c = int(stdout.readline().replace('\n', '').strip())
            if c > 0:
                rprint(f"[bold green]\[PASSED][/bold green] The process is running. - '{process}'")
            else:
                is_passed = Result.FAILED.value
                rprint(f"[bold red]\[FAILED][/bold red] The process is not running. - '{process}'")

        ports = server['assertThat']['ports']
        for port in ports:
            stdin, stdout, stderr = instance.exec_command(commando.cmd['port'].format(int(port)))
            c = int(stdout.readline().replace('\n', '').strip())
            if c > 0:
                rprint(f"[bold green]\[PASSED][/bold green] The port is opened. - '{port}'")
            else:
                is_passed = Result.FAILED.value
                rprint(f"[bold red]\[FAILED][/bold red] The port is not opened. - '{port}'")

        results.append([idx + 1, server['id'], name, private_ip, is_passed])
        rprint("")
    _report(results)


def _report(data: list):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta", title="View Test Report")
    table.width = console.width
    table.box = box.SIMPLE_HEAD
    table.pad_edge = False
    table.add_column("No", style="dim", width=5, justify="right")
    table.add_column("UUID")
    table.add_column("Server name")
    table.add_column("Private IP")
    table.add_column("Result")

    for value in data:
        table.add_row(str(value[0]), value[1], value[2], value[3], str(value[4]))

    console.print(table)

# @TODO
# def ssh_jump():
        # print(f"Assertion is complete.\n")

        # TO-DO
        # assert int(exported_port) == server['assertThat']['resources']['ports'], ""
        # assert processes

    # paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

    # proxy_command = paramiko.ProxyCommand(
    #     f"ssh -i ~/set-shared-keypair.pem -W {vm_ip}:22 {bastion_host_user}@{bastion_host_ip}"
    # )
    # proxy.settimeout(300)
    # print(proxy_command.cmd)

    # vm_keypair = server['keypair']

    # print(f"-----> Connect to the bastion host")
    # pdb.set_trace()
    # ssh.connect(vm_ip, username=vm_user, allow_agent=True, pkey=private_key, sock=proxy_command)
    # print(f"-----> Connected to the bastion host")

    # connect to  virtual machine through bastion host
    # stdin, stdout, stderr = ssh.exec_command(f"hostname")
    # print(f">>> 1 >>> {stdout.readline()}")


#
# stdin, stdout, stderr = ssh.exec_command(f"ssh -i {vm_keypair} {vm_user}@{vm_ip}")
# print(f">>> 1 >>> {stdout.readline()}")
# stdin.write(f"sudo -i\n")
# print(f">>> 2 >>> {stdout.readline()}")
# stdin.write(f"hostname")
# print(f">>> 3 >>> {stdout.readline()}")

def _upAndClear(cnt):
    for idx in range(cnt):
        print(LINE_UP, end=LINE_CLEAR)


def _gib(size: int) -> int:
    return utils.gib(size)


if __name__ == '__main__':
    print(template_dir)

