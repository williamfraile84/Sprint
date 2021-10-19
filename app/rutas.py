from main import app
from flask import request,render_template, redirect, url_for, jsonify, session
from app.forms import loginForm, registerForm
from app.datosPerfil import publicaciones, amigos
from app.db import select_db, insert_db
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = loginForm(request.form)
    title = 'Iniciar Sesión'
    if request.method == 'POST' and form_login.validate():
        usuario = request.form['usuario']
        clave = request.form['contraseña']

        consulta = select_db(usuario)
        if len(consulta)==0:
            print('ERROR: Usuario o clave invalidas')
            return render_template('login.html', title = title, formLog = form_login)
        else:
            contraseña = consulta[0][1]
            if check_password_hash(contraseña, clave):
                print('Formulario Exitoso')
                return redirect(url_for('dashboard'))
            else:
                print('ERROR: Usuario o clave invalidas')
                return render_template('login.html', title = title, formLog = form_login)
    else:
        print('Error en el formulario')
    return render_template('login.html', title = title, formLog = form_login)

@app.route('/register', endpoint='register',methods=['GET', 'POST'])
def register():
    form_register = registerForm(request.form)
    title = 'Registrarse'
    if request.method == 'POST' and form_register.validate():
        nombre = request.form['nombre'] + request.form['apellido']
        usuario = request.form['usuario']
        email = request.form['email']
        clave = request.form['contraseña']
        fechaNacimiento = request.form['dia']+'-'+ request.form['mes']+'-'+ request.form['año']
        sexo = request.form['sexo']

        contraseña = generate_password_hash(clave)
        insert_db(nombre,usuario,email,contraseña,fechaNacimiento,sexo)
        print('Formulario Exitoso')
        return redirect(url_for('login'))
    # else:
    #     print('Error en el formulario')
    return render_template('register.html', title = title, formReg = form_register)

@app.route('/dashboard')
def dashboard():
    title = 'Dashboard'
    return render_template('dashboard.html', title=title)

@app.route('/profile')
def profile():
    title = 'Perfil Usuario'
    return render_template('profile.html', title=title, publicacion=publicaciones, amigo=amigos)

@app.route('/articulos')
def listar_articulos():
    return jsonify({'publicacion':publicaciones})