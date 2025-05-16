from flask import Flask, request, render_template
from main import ConexionSFTP

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar_archivo', methods=['POST'])
def enviar_archivo():
    conexion = ConexionSFTP('192.168.1.10', 'Usuario', '123456')
    conexion.enviar_archivo('C:/Users/Usuario/Desktop/shockie/sftp-implementacion/archivo.txt')
    return 'Archivo enviado'