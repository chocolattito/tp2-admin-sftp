from flask import Flask, request, render_template, redirect, url_for, session , flash
from main import ConexionSFTP

app = Flask(__name__)
app.secret_key = "clave_super_secreta"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conexion_info = {
            'hostname': request.form['hostname'],
            'username': request.form['username'],
            'password': request.form['password']
        }
        session['conexion_info'] = conexion_info
        # Aca se crea una instancia de la clase conexionSFTP
        session['message'] = "Conexión establecida!"
        return redirect(url_for('index'))
    conexion_data = session.pop('conexion_info', None)
    message = session.pop('message', None)
    return render_template('index.html', conexion=conexion_data, message=message)


@app.route('/enviar_archivo', methods=['GET', 'POST'])
def enviar_archivo():
    if request.method == 'POST':
        'ruta_archivo' == request.files["archivo"].filename
        return redirect(url_for('index', message='Archivo enviado!'))
    return render_template('enviar_archivo.html')

@app.route('/listar_archivos', methods=['GET', 'POST'])
def listar_archivos():
    archivos = session.get('archivos', [])
    if request.method == 'POST':
        pass
    return render_template('listar_archivos.html', archivos=archivos)

@app.route('/descargar_archivo', methods=['GET', 'POST'])
def descargar_archivo():
    if request.method == 'POST':
        pass # lógica de descarga aquí
    return render_template('descarga.html')

@app.route('/borrar_archivo', methods=['GET', 'POST'])
def borrar_archivo():
    if request.method == 'POST':
        pass # lógica de borrado aquí
    return render_template('borrar.html')

@app.route('/desconectar', methods=['GET', 'POST'])
def desconectar():
    return render_template('index.html', conexion=None, message=None)

if __name__ == "__main__":
    app.run(debug=True)
