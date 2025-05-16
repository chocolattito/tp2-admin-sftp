from flask import Flask, request, render_template, redirect, url_for
from main import ConexionSFTP


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    archivos=["archivo1.txt", "archivo2.txt", "archivo3.txt"]
    if request.method == 'POST':
        return redirect(url_for('listar_archivos', listaDeArchivos=archivos))
    else:
        return render_template('index.html')

@app.route('/enviar_archivo', methods=['POST'])
def enviar_archivo():
    conexion = ConexionSFTP('192.168.1.10', 'Usuario', '123456')
    conexion.enviar_archivo('C:/Users/Usuario/Desktop/shockie/sftp-implementacion/archivo.txt')
    return 'Archivo enviado'

@app.route('/listar_archivos', methods=['GET', 'POST'])
def listar_archivos():
    if request.method == "GET":
        return redirect(url_for('index'))
    else:
        render_template('listar_archivos.html')

if __name__ == "__main__":
    app.run(debug=True)