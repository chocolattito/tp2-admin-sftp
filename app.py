# pylint:disable=C0116,C0115,C0114,C0103,W0718,W0603

import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from conexion_sftp import ConexionSFTP

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

conexion_info = None


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Maneja la conexión SFTP. Si es un POST, intenta conectar;
    si es GET, muestra el formulario de conexión o las acciones si ya está conectado.
    """

    if request.method == 'POST':
        localname = request.form['localname']
        hostname = request.form['hostname']
        username = request.form['username']
        password = request.form['password']

        global conexion_info
        conexion_info = {
            "localname": localname,
            "hostname": hostname,
            "username": username,
            "password": password
        }

        try:
            ConexionSFTP(conexion_info)

            flash("Conexión SFTP establecida con éxito.", "success")
            return redirect(url_for('index')) # Redirigir para evitar reenvío de formulario
        except Exception as e:
            print(e)

            # Si hay un error, limpiar cualquier información de conexión fallida
            conexion_info = None
            flash("Error al intentar establecer la conexión:", "danger")
            return redirect(url_for('index'))

    if conexion_info is not None:
        return render_template('index.html', conexion=conexion_info)

    return render_template('index.html', conexion=None) # Mostrar el formulario de conexión

@app.route('/enviar_archivo', methods=['GET', 'POST'])
def enviar_archivo():
    """
    El usuario utilizando un formulario, sube un archivo dando la ruta y luego se manda al servidor.
    """

    if conexion_info is  None:
        return redirect(url_for('index'))

    if request.method == 'POST':

        try:
            if 'archivo' not in request.files:
                raise ValueError("No existe el archivo")
            archivo = request.files['archivo']
            if archivo.filename == '':
                raise ValueError("No se seleccionó un archivo")
            if archivo and archivo.filename:
                filename = secure_filename(archivo.filename)
                file_path = os.path.join('./subida', filename)
                abs_path = os.path.abspath(file_path)
                archivo.save(file_path)
                print(abs_path)
                ConexionSFTP().enviar_archivo(abs_path)
                os.remove(file_path)
                flash(f"Archivo '{archivo.filename}' enviado con éxito.", "success")
        except Exception as e:
            print(e)
            flash("Error al enviar el archivo", "danger")

        return redirect(url_for('index'))
    return render_template('enviar_archivo.html')

@app.route('/listar_archivos', methods=['GET', 'POST'])
def listar_archivos():
    """
    El usuario vizualiza la lista de archivos en el servidor.
    """

    if conexion_info is  None:
        return redirect(url_for('index'))

    archivos = ConexionSFTP().listar_archivos()

    return render_template('listar_archivos.html', archivos=archivos)

@app.route('/descargar_archivo', methods=['GET', 'POST'])
def descargar_archivo():
    """ 
    El usuario descarga un archivo del servidor.
    """

    if conexion_info is  None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            archivo = request.form["archivo_a_descargar"]
            ConexionSFTP().descargar_archivo(archivo)
            flash(f"Archivo '{archivo}' descargado con éxito.", "success")
        except Exception as e:
            print(e)
            flash("Error al descargar el archivo", "danger")

        return redirect(url_for('index'))

    archivos = ConexionSFTP().listar_archivos()

    return render_template('descarga.html', archivos=archivos)

@app.route('/borrar_archivo', methods=['GET', 'POST'])
def borrar_archivo():
    """ 
    El usuario borra un archivo del servidor.
    """

    if conexion_info is  None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            archivo = request.form["archivo_a_borrar"]
            ConexionSFTP().borrar_archivo(archivo)
            flash(f"Archivo '{archivo}' borrado con éxito.", "success")
        except Exception as e:
            print(e)
            flash("Error al descargar el archivo", "danger")

    archivos = ConexionSFTP().listar_archivos()

    return render_template('borrar.html', archivos=archivos)

@app.route('/desconectar', methods=['GET', 'POST'])
def desconectar():
    """ 
    El usuario desconecta de la conexión SFTP.
    """

    global conexion_info
    if conexion_info is not None:
        conexion_info = None
        try:
            ConexionSFTP().desconectar()
        except Exception as e:
            print(e)

    flash("Sesión SFTP cerrada correctamente.", "info")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
