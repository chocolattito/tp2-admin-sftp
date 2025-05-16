import paramiko

class ConexionSFTP:
    DEFAULT_PORT = 22
    DEFAULT_DIRECTORY = 'C:/SFTPImplement'

    def __init__(
            self, hostname: str, username: str, password: str,
            port: int=DEFAULT_PORT, directory: str = DEFAULT_DIRECTORY):
        self.__HOSTNAME = hostname
        self.__PORT = port
        self.__USERNAME = username
        self.__PASSWORD = password
        self.__DIRECTORY = directory

        # clientes
        self.__SSH_CLIENT = self.__init_ssh_client()
        self.__SFTP_CLIENT = self.__init_sftp_client(self.__SSH_CLIENT)

    def __del__(self):
        self.__SFTP_CLIENT.close()
        self.__SSH_CLIENT.close()

    def __init_ssh_client(self) -> paramiko.SSHClient:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys(f'C:/Users/{self.__USERNAME}/.ssh/known_hosts')
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.__HOSTNAME, self.__PORT, self.__USERNAME, self.__PASSWORD)
        return ssh_client

    def __init_sftp_client(self, ssh_client: paramiko.SSHClient) -> paramiko.SFTPClient:
        sftp_client = ssh_client.open_sftp()
        return sftp_client

    def enviar_archivo(self, directorio_arch: str) -> None:
        arch_local = directorio_arch
        arch_remoto = (self.__DIRECTORY + "/archivotest")
        self.__SFTP_CLIENT.put(arch_local, arch_remoto)

    def descargar_archivo(self, directorio_local: str) -> None:
        arch_local = directorio_local
        arch_remoto = (self.__DIRECTORY + "/archivotest")
        self.__SFTP_CLIENT.get(arch_remoto, arch_local)
                                                                                                                                                                                   
    def listar_archivos(self) -> list[str]:
        archivos = self.__SFTP_CLIENT.listdir(self.__DIRECTORY)
        return archivos
