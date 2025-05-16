from flask import Flask, request, render_template, redirect, url_for, session
from main import ConexionSFTP

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

@app.route('/', methods=['GET', 'POST'])
def index():
    archivos = ["archivo1.txt", "archivo2.txt", "archivo3.txt"]
    if request.method == 'POST':        # Guardamos la lista de archivos en la sesión
        session['archivos'] = archivos
        return redirect(url_for('listar_archivos'))
    return render_template('index.html')

@app.route('/enviar_archivo', methods=['GET', 'POST'])
def enviar_archivo():
    if request.method == 'POST':
        pass  # lógica de envío aquí
    return render_template('enviar_archivo.html')  # ¡Faltaba return!

@app.route('/listar_archivos', methods=['GET', 'POST'])
def listar_archivos():
    archivos = session.get('archivos', [])
    if request.method == 'POST':
        pass
    return render_template('listar_archivos.html', archivos=archivos)

@app.route('/descargar_archivo', methods=['GET', 'POST'])
def descargar_archivo():
    if request.method == 'POST':
        pass

    return render_template('descarga.html')

@app.route('/borrar_archivo', methods=['GET', 'POST'])
def borrar_archivo():
    if request.method == 'POST':
        pass
  
    return render_template('borrar.html')

if __name__ == "__main__":
    app.run(debug=True)
