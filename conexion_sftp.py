# pylint:disable=C0116,C0115,C0114,C0103

import re
import paramiko

class ConexionSFTP:
    _instance = None
    _connected = False

    DEFAULT_PORT = 22

    DEFAULT_PATH = '/SFTPImplement'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
            self, data: dict[str, str]=None, port: int=DEFAULT_PORT # type: ignore
    ):
        if self._connected is False:
            self.__local_username = data['localname']
            self.__hostname = data['hostname']
            self.__username = data['username']
            self.__password = data['password']
            self.__port = port

            self.__path = f'/home/{self.__username}{self.DEFAULT_PATH}'
            self.__path_local = f'/Users/{self.__local_username}{self.DEFAULT_PATH}'

            # clientes
            self.__ssh_client = self.__init_ssh_client()
            self.__sftp_client = self.__init_sftp_client(self.__ssh_client)

            self._connected = True

    def __del__(self):
        self.__sftp_client.close()
        self.__ssh_client.close()

    def __init_ssh_client(self) -> paramiko.SSHClient:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.__hostname, self.__port, self.__username, self.__password)
        return ssh_client

    def __init_sftp_client(self, ssh_client: paramiko.SSHClient) -> paramiko.SFTPClient:
        sftp_client = ssh_client.open_sftp()
        #sftp_client.mkdir(self.__path)
        return sftp_client

    def enviar_archivo(self, arch_local: str) -> None:
        arch_local_re = re.search(r'^/(.+/)*(.+)\.(.+)$' , arch_local)
        arch_local_nombre = f"{arch_local_re[2]}.{arch_local_re[3]}" # type: ignore
        arch_remoto = self.__path + "/" + arch_local_nombre
        self.__sftp_client.put(arch_local, arch_remoto)

    def descargar_archivo(self, arch_remoto_nombre: str) -> None:
        arch_remoto = self.__path + "/" + arch_remoto_nombre
        arch_local = self.__path_local + "/" + arch_remoto_nombre
        self.__sftp_client.get(arch_remoto, arch_local)

    def listar_archivos(self) -> list[str]:
        archivos = self.__sftp_client.listdir(self.__path)
        return archivos

    def borrar_archivo(self, arch_remoto_nombre: str) -> None:
        arch_remoto = self.__path + "/" + arch_remoto_nombre
        self.__sftp_client.remove(arch_remoto)
