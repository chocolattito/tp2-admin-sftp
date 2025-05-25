from flask import Flask, request, render_template, redirect, url_for, session, flash
from main import ConexionSFTP  # Asegúrate de que esto no cause errores si lo estás simulando

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

        # Simulación de éxito o error:
        if conexion_info['hostname']:  # Simulamos que si hay host, se conecta
            flash("Conexión establecida con éxito.", "success")
        else:
            flash("Error en la conexión, intente de nuevo.", "error")

        return redirect(url_for('index'))

    conexion_data = session.get('conexion_info')
    return render_template('index.html', conexion=conexion_data)

@app.route('/enviar_archivo', methods=['GET', 'POST'])
def enviar_archivo():
    if request.method == 'POST':
        archivo = request.files.get("archivo")
        if archivo and archivo.filename:
            flash(f"Archivo '{archivo.filename}' enviado con éxito.", "success")
        else:
            flash("No se seleccionó ningún archivo.", "error")
        return redirect(url_for('index'))
    return render_template('enviar_archivo.html')

@app.route('/listar_archivos', methods=['GET', 'POST'])
def listar_archivos():
    archivos = session.get('archivos', ["archivo1.txt", "archivo2.pdf"])  # Simulados
    if request.method == 'POST':
        flash("Archivos listados correctamente.", "success")
    return render_template('listar_archivos.html', archivos=archivos)

@app.route('/descargar_archivo', methods=['GET', 'POST'])
def descargar_archivo():
    if request.method == 'POST':
        flash("Archivo descargado con éxito.", "success")
        return redirect(url_for('index'))
    archivos = session.get('archivos', ["archivo1.txt", "archivo2.pdf"])  # Simulados
    return render_template('descarga.html', archivos=archivos)

@app.route('/borrar_archivo', methods=['GET', 'POST'])
def borrar_archivo():
    if request.method == 'POST':
        flash("Archivo borrado correctamente.", "success")
        return redirect(url_for('index'))
    archivos = session.get('archivos', ["archivo1.txt", "archivo2.pdf"])  # Simulados
    return render_template('borrar.html', archivos=archivos)

@app.route('/desconectar', methods=['GET', 'POST'])
def desconectar():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
