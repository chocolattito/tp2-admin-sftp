# Protocolo SFTP - C1 TP2 Admin. de Sistemas y Redes
Proyecto de investigación e implementación del protocolo SFTP (SSH File Transfer Protocol) para el segundo trabajo práctico de primer cuatrimestre en Administración de Sistemas y Redes.

Desarrollado por **Sebastian Daniel Marcos** y **Tomas Valentin Muruchi**, 6°AO.

Una demo de la implementación se puede ver [acá](https://drive.google.com/file/d/1ZdbkGGUDQnIWaGJ7soSX7IJJZhtFUgG7/view?usp=sharing).
## Requerimientos y dependencias
Por simplicidad, el software fue pensado para ser utilizado entre dos sistemas Linux, uno que actua como cliente y el otro como servidor.
### Prerequisitos cliente y servidor
El software almacena archivos del lado cliente y servidor en un directorio "SFTPImplement" predefinido que debe ser creado manualmente y ubicado en el directorio "home" del usuario cliente y el usuario servidor.
```
mkdir /home/[Nombre de usuario]/SFTPImplement
```
### Servidor (Debian/Ubuntu)
Los siguientes comandos aplican para sistemas Debian, Ubuntu o derivados que utilicen el gestor de paquetes APT. La instalación y la activación del servidor SSH puede variar dependiendo de la distro de Linux que se utilice.
#### Servidor SSH
```
sudo apt install openssh-server
```
```
sudo systemctl enable ssh
```
```
sudo systemctl start ssh
```
### Cliente
Requiere una instalación de Python en el sistema para funcionar.
#### Virtual environment
(claramente... :P)
```
python3 -m venv venv
```
```
source ./venv/bin/activate
```
#### Paramiko
Implementación del protocolo SSHv2.2 para Python que ofrece funcionalidades tanto de cliente como de servidor, incluyendo la funcionalidad SFTP.
```
pip install paramiko
```
#### Flask
Framework ligero de frontend para la interacción del usuario final con el sistema a través de formularios HTML.
```
pip install flask
```
#### Ejecución
Ejecuta el software de cliente. Una vez corriendo el software, estará disponible en su IP local http://127.0.0.1:5000 donde deberá entrar con un navegador web.
```
python3 app.py
```
Para realizar una conexión, deberá conocer el nombre de usuario del sistema cliente, la dirección IP del servidor y las credenciales de usuario del servidor.
<img width="1343" alt="image" src="https://github.com/user-attachments/assets/b80c5b06-5f3c-4efb-8fbd-d39a20c1aced" />

