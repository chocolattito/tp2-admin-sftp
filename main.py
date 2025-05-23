# pylint:disable=C0116,C0115,C0114,C0103

import re
import paramiko

class ConexionSFTP:
    DEFAULT_PORT = 22

    DEFAULT_PATH = '/SFTPImplement'
    DEFAULT_SSH = '/.ssh/known_hosts'

    def __init__(
            self, localusername: str, hostname: str, username: str, password: str,
            port: int=DEFAULT_PORT
    ):
        self.__LOCAL_USERNAME = localusername
        self.__HOSTNAME = hostname
        self.__PORT = port
        self.__USERNAME = username
        self.__PASSWORD = password

        self.__path = f'/home/{self.__USERNAME}{self.DEFAULT_PATH}'
        self.__path_local = f'/home/{self.__LOCAL_USERNAME}{self.DEFAULT_PATH}'

        # clientes
        self.__ssh_client = self.__init_ssh_client()
        self.__sftp_client = self.__init_sftp_client(self.__ssh_client)

    def __del__(self):
        self.__sftp_client.close()
        self.__ssh_client.close()

    def __init_ssh_client(self) -> paramiko.SSHClient:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.__HOSTNAME, self.__PORT, self.__USERNAME, self.__PASSWORD)
        return ssh_client

    def __init_sftp_client(self, ssh_client: paramiko.SSHClient) -> paramiko.SFTPClient:
        sftp_client = ssh_client.open_sftp()
        sftp_client.mkdir(self.__path)
        return sftp_client

    def enviar_archivo(self, arch_local: str) -> None:
        arch_local_re = re.search(r'^\\(.+\\)*(.+)\.(.+)$' , arch_local)
        arch_local_nombre = arch_local_re[2] + arch_local_re[3] # type: ignore
        arch_remoto = self.__path + "/" + arch_local_nombre
        self.__sftp_client.put(arch_local, arch_remoto)

    def descargar_archivo(self, arch_remoto_nombre: str) -> None:
        arch_remoto = self.__path + "/" + arch_remoto_nombre
        arch_local = self.__path_local + "/" + arch_remoto_nombre
        self.__sftp_client.get(arch_remoto, arch_local)

    def listar_archivos(self) -> list[str]:
        archivos = self.__sftp_client.listdir(self.__path)
        return archivos
