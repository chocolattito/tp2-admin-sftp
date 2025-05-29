# Protocolo SFTP - C1 TP2 Admin. de Sistemas y Redes
Proyecto de investigación y implementación del protocolo SFTP (SSH File Transfer Protocol) para el segundo trabajo práctico de primer cuatrimestre en Administración de Sistemas y Redes.

Desarrollado por **Sebastian Daniel Marcos** y **Tomas Valentin Muruchi**, 6°AO.
## Requerimientos y dependencias
Por simplicidad, el software fue pensado para ser utilizado entre dos sistemas Linux, uno que actua como cliente y el otro como servidor.
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
Ejecuta el software de cliente. Una vez corriendo el software, estará disponible en su IP local http://127.0.0.1:5000
```
py app.py
```
### Servidor (Ubuntu)
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
