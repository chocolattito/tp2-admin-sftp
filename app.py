# pylint:disable=C0116,C0115,C0114,C0103,W0718

from flask import Flask, request, render_template, redirect, url_for, session, flash
from conexion_sftp import ConexionSFTP

app = Flask(__name__)
app.secret_key = "clave_super_secreta"


def get_sftp_client():
    """
    Función auxiliar para obtener la instancia de ConexionSFTP desde la sesión.
    Si no existe o la conexión se perdió, redirige al inicio. 
    Sirve para evitar de que se pueda acceder a las funciones sin tener alguna conexionl.
    """
    conexion_info = session.get('conexion_info')
    conexion_object = session.get('conexion_object')

    if not conexion_info or not conexion_object:
        flash("No hay conexión SFTP activa. Por favor, conéctate primero.", "warning")
        return None, None # Retorna None para que la ruta pueda redirigir

    return conexion_object, conexion_info


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

        session['conexion_info'] = {
            'localname': localname,
            'hostname': hostname,
            'username': username,
            'password': password 
        }

        try:
            ConexionSFTP(session['conexion_info'])

            flash("Conexión SFTP establecida con éxito.", "success")
            return redirect(url_for('index')) # Redirigir para evitar reenvío de formulario
        except Exception as e:
            print(e)

            # Si hay un error, limpiar cualquier información de conexión fallida
            session['conexion_info'] = None
            session['archivos_remotos'] = None
            flash("Error al intentar establecer la conexión:", "danger")
            return redirect(url_for('index'))

    conexion_data = session.get('conexion_info')

    if conexion_data is not None:
        return render_template('index.html', conexion=conexion_data, archivos=session.get('archivos_remotos', []))
    else:
        return render_template('index.html', conexion=None) # Mostrar el formulario de conexión

@app.route('/enviar_archivo', methods=['GET', 'POST'])
def enviar_archivo():
    """
    El usuario utilizando un formulario, sube un archivo dando la ruta y luego se manda al servidor.
    """

    conexion_info = session.get('conexion_info')
    if conexion_info is  None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        archivo = request.files.get("archivo")

        try:
            ConexionSFTP().enviar_archivo(archivo.filename)
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

    conexion_info = session.get('conexion_info')
    if conexion_info is  None:
        return redirect(url_for('index'))

    archivos = ConexionSFTP().listar_archivos()

    return render_template('listar_archivos.html', archivos=archivos)

@app.route('/descargar_archivo', methods=['GET', 'POST'])
def descargar_archivo():
    """ 
    El usuario descarga un archivo del servidor.
    """

    conexion_info = session.get('conexion_info')
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

    conexion_info = session.get('conexion_info')
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

    conexion_object = session.pop('conexion_object', None)
    if conexion_object:
        try:
            conexion_object.desconectar() # Llamar al método desconectar del objeto SFTP
        except Exception as e:
            print(f"Error al cerrar la conexión SFTP") # Imprimir en consola, no flashear al usuario
    
    session.clear() # Limpiar toda la sesión
    flash("Sesión SFTP cerrada correctamente.", "info")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
