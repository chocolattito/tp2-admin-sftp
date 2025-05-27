from flask import Flask, request, render_template, redirect, url_for, session, flash
from main import ConexionSFTP

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
        hostname = request.form['hostname']
        username = request.form['username']
        password = request.form['password']

        session['conexion_info'] = {
            'hostname': hostname,
            'username': username,
            'password': password 
        }

        try:

            conexion = ConexionSFTP(hostname, username, password)
            conexion.conectar() # Intentar conectar

            session['conexion_object'] = conexion # Almacenar el objeto completo

            flash("Conexión SFTP establecida con éxito.", "success")
            return redirect(url_for('index')) # Redirigir para evitar reenvío de formulario
        except Exception as e:
            # Si hay un error, limpiar cualquier información de conexión fallida
            session.pop('conexion_info', None)
            session.pop('conexion_object', None)
            session.pop('archivos_remotos', None)
            flash(f"Error al intentar establecer la conexión:", "danger")
            return redirect(url_for('index'))

    conexion_data = session.get('conexion_info')
    
    if 'conexion_object' in session:
        return render_template('index.html', conexion=conexion_data, archivos=session.get('archivos_remotos', []))
    else:
        return render_template('index.html', conexion=None) # Mostrar el formulario de conexión

@app.route('/enviar_archivo', methods=['GET', 'POST'])
def enviar_archivo():
    """
    El usuario utilizando un formulario, sube un archivo dando la ruta y luego se manda al servidor.
    """

    conexion_object, conexion_info = get_sftp_client()
    if not conexion_object:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        archivo = request.files.get("archivo")

        try:
            conexion_object.enviar_archivo(archivo.filename)
            flash(f"Archivo '{archivo.filename}' enviado con éxito.", "success")
        except Exception as e:
            flash(f"Error al enviar el archivo", "danger")

        return redirect(url_for('index'))
    return render_template('enviar_archivo.html')

@app.route('/listar_archivos', methods=['GET', 'POST'])
def listar_archivos():
    """
    El usuario vizualiza la lista de archivos en el servidor.
    """

    conexion_object, conexion_info = get_sftp_client()
    if not conexion_object:
        return redirect(url_for('index'))

    return render_template('listar_archivos.html', archivos=conexion_object.listar_archivos())

@app.route('/descargar_archivo', methods=['GET', 'POST'])
def descargar_archivo():
    """ 
    El usuario descarga un archivo del servidor.
    """

    if request.method == 'POST':

        try:
            conexion_object.descargar_archivo(archivo.filename)
            flash(f"Archivo '{archivo.filename}' descargado con éxito.", "success")
        except Exception as e:
            flash(f"Error al descargar el archivo", "danger")

        return redirect(url_for('index'))

    return render_template('descarga.html', archivos=conexion_object.listar_archivos())

@app.route('/borrar_archivo', methods=['GET', 'POST'])
def borrar_archivo():
    """ 
    El usuario borra un archivo del servidor.
    """

    conexion_object, conexion_info = get_sftp_client()
    if not conexion_object:
        return redirect(url_for('index'))

    if request.method == 'POST':
        flash("Archivo borrado correctamente.", "success")
        return redirect(url_for('index'))
    
    return render_template('borrar.html', archivos=conexion_object.listar_archivos())

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
