from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import mysql.connector


# Crear la aplicación Flask
app = Flask(__name__)

# Configurar SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:q1w2e3r4t5@localhost/planetasapiens'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Conexión a la base de datos con mysql.connector
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="q1w2e3r4t5",
    database="planetasapiens"
)

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'usuarios'
    idUsuarios = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido_pa = db.Column(db.String(45), nullable=False)
    apellido_ma = db.Column(db.String(45), nullable=False)
    correo = db.Column(db.String(45), nullable=False)
    fecha_ingreso = db.Column(db.Date, nullable=False)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.idTipo_usuario'), nullable=False)
    tipo_usuario = db.relationship('TipoUsuario', backref='usuarios')

# Modelo de Tipo de Usuario
class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    idTipo_usuario = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(45), nullable=False)

# Modelo de Curso
class Curso(db.Model):
    __tablename__ = 'curso'
    idCurso = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)
    contenido = db.Column(db.String(45))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuarios'), nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False, default=date.today)
    estatus = db.Column(db.Integer, nullable=False, default=1)

# Rutas
@app.route('/')
def index():
    tipos_usuarios = [
        {'idTipo_usuario': 1, 'descripcion': 'Administrador'},
        {'idTipo_usuario': 2, 'descripcion': 'Usuario_n'}
    ]
    return render_template('index.html', tipos_usuarios=tipos_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aquí iría la lógica para autenticar al usuario desde la base de datos
        return redirect(url_for('dashboard'))  # Redirecciona al dashboard después del login
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        apellido_pa = request.form['apellido_pa']
        apellido_ma = request.form['apellido_ma']
        id_tipo_usuario = int(request.form['id_tipo_usuario'])

        # Crear un nuevo usuario y guardarlo en la base de datos
        new_user = User(
            nombre=username,
            apellido_pa=apellido_pa,
            apellido_ma=apellido_ma,
            correo=email,
            fecha_ingreso='2024-07-10',  # Aquí deberías establecer la fecha actual o la fecha que desees
            id_tipo_usuario=id_tipo_usuario
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))  # Redirecciona al inicio después de registrar usuario

    # Obtener todos los tipos de usuario para enviarlos al formulario de registro
    tipos_usuarios = TipoUsuario.query.all()

    return render_template('register.html', tipos_usuarios=tipos_usuarios)

@app.route('/eliminar_curso/<int:id_curso>', methods=['POST'])
def eliminar_curso(id_curso):
    curso = Curso.query.get_or_404(id_curso)
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Aquí deberías implementar la lógica para verificar el tipo de usuario y mostrar el dashboard correspondiente
    cursos = Curso.query.all()  # Obtener todos los cursos, por ejemplo
    return render_template('dashboard.html', cursos=cursos)

@app.route('/agregar_curso', methods=['GET', 'POST'])
def agregar_curso():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        id_usuario = 1  # Ejemplo: deberías obtener el id del usuario logueado desde la sesión
        fecha_publicacion = date.today()  # Fecha actual
        estatus = 1  # Por defecto activo

        # Crear un nuevo curso y guardarlo en la base de datos
        new_curso = Curso(
            titulo=titulo,
            contenido=contenido,
            id_usuario=id_usuario,
            fecha_publicacion=fecha_publicacion,
            estatus=estatus
        )
        db.session.add(new_curso)
        db.session.commit()

        return redirect(url_for('dashboard'))  # Redirecciona al dashboard después de agregar curso

    return render_template('agregar_curso.html')

if __name__ == '__main__':
    app.run(debug=True)
