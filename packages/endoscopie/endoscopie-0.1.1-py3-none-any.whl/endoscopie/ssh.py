import io
import os.path

import paramiko
from endoscopie.logarithm import Logarithm
from paramiko.pkey import PKey

logger = Logarithm(__name__)


class EndoscopieSSHClient:
    def __init__(self):
        self.hostname = None
        self.username = None
        self.keypair = None
        self.sock = None

        self.ssh_client = paramiko.SSHClient()


    def get_key_object(self, keypair) -> PKey:
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with open(os.path.abspath(keypair)) as keyfile:
            key = keyfile.read()

        private_key = paramiko.RSAKey.from_private_key(io.StringIO(key))
        return private_key


    def connect(self, hostname, username, keypair, sock=None) -> None:
        """
         :param hostname: str
             The instance IP(v4)
        :param username: str
            OS username
            ex)
               Ubuntu -> ubuntu
               CentOS and CentOS Stream -> centos
               Rocky Linux -> rocky
               Almalinux -> almalinux
        :param keypair: paramiko.pkey.PKey
            Path to the private key object for ssh connection
         :param socket sock:
            an open socket or socket-like object (such as a `.Channel`) to use for communication to the target host

        :return: None
        """
        logger.debug(f"hostname: {hostname}")
        logger.debug(f"username: {username}")
        self.hostname = hostname
        self.username = username
        self.keypair = keypair
        self.sock = sock

        if (self.hostname is None) or (self.username is None) or (self.keypair is None):
            logger.error("These values are required. ['hostname', 'username', 'keypair']")
            return

        self._connect_direct(self.hostname, self.username, self.keypair, self.sock)


    def exec_command(self, command):
        logger.debug(f"exec command : {command}")
        return self.ssh_client.exec_command(command=command)


    def get_transport(self):
        logger.debug("The `.Transport` object for this SSH connection.")
        return self.ssh_client.get_transport()


    def _connect_direct(self, hostname, username, keypair, sock):
        logger.debug("Connect to an SSH server and authenticate to it.")
        self.ssh_client.connect(hostname=hostname, username=username, pkey=keypair, sock=sock)



