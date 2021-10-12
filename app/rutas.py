from main import app
from flask import request,render_template, redirect, url_for
from app.forms import loginForm, registerForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = loginForm(request.form)
    title = 'Iniciar Sesión'
    if request.method == 'POST' and form_login.validate():
        print('Formulario Exitoso')
        return redirect(url_for('dashboard'))
    else:
        print('Error en el formulario')
    return render_template('login.html', title = title, formLog = form_login)

@app.route('/register', endpoint='register',methods=['GET', 'POST'])
def register():
    form_register = registerForm(request.form)
    title = 'Registrarse'
    if request.method == 'POST' and form_register.validate():
        print('Formulario Exitoso')
        return redirect(url_for('login'))
    else:
        print('Error en el formulario')
    return render_template('register.html', title = title, formReg = form_register)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    title = 'Perfil Usuario'
    return render_template('profile.html', title=title)