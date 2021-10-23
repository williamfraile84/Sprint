from main import app
from flask import request, render_template, redirect, url_for, jsonify, session
from app.forms import loginForm, registerForm
from flask.helpers import make_response
from app.datosPerfil import publicaciones, amigos, comentarios
from app.db import select_db, insert_db, select_db_publicacion, pruebas, delete_pub_db, delete_com_db, update_com_db, insert_com_db, select_db_perfil, select_perfil_db, perfil_db,img_perfil_db,select_img_perfil_db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from main import os
from main import hashlib
from string import ascii_letters,digits
from random import choice
from datetime import timedelta


@app.route('/ip')
def ip():
    session['ip'] = request.remote_addr
    response = make_response(redirect('/cookie'))
    response.set_cookie('nombre_cliente', 'MisionTic')
    return response


@app.route('/cookie')
def cookie():
    if session.get('id'):
        ip = session['ip']
    else:
        ip = 'nula'

    nombre_cliente = request.cookies.get('nombre_cliente')
    if nombre_cliente == None:
        nombre_cliente = 'N/A'
    return f'tu ip es {ip} y tu nombre es {nombre_cliente}'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = loginForm(request.form)
    title = 'Iniciar Sesión'
    if request.method == 'POST' and form_login.validate():
        usuario = request.form['usuario']
        clave = request.form['contraseña']

        consulta = select_db(usuario)
        if len(consulta) == 0:
            print('ERROR: Usuario o clave invalidas')
            return render_template('login.html', title=title, formLog=form_login)
        else:
            contraseña = consulta[0][2]
            if check_password_hash(contraseña, clave):
                session.clear()
                session['id'] = consulta[0][0]
                session['usr'] = usuario
                session['cla'] = clave
                print('Formulario Exitoso')
                return redirect(url_for('dashboard'))
            else:
                print('ERROR: Usuario o clave invalidas')
                return render_template('login.html', title=title, formLog=form_login)
    else:
        print('Error en el formulario')
    return render_template('login.html', title=title, formLog=form_login)


@app.route('/register', endpoint='register', methods=['GET', 'POST'])
def register():
    form_register = registerForm(request.form)
    title = 'Registrarse'
    if request.method == 'POST' and form_register.validate():
        nombre = request.form['nombre'] + request.form['apellido']
        usuario = request.form['usuario']
        email = request.form['email']
        clave = request.form['contraseña']
        fechaNacimiento = request.form['dia']+'-' + \
            request.form['mes']+'-' + request.form['año']
        sexo = request.form['sexo']

        contraseña = generate_password_hash(clave)
        insert_db(nombre, usuario, email, contraseña, fechaNacimiento, sexo)
        print('Formulario Exitoso')
        return redirect(url_for('login'))
    # else:
    #     print('Error en el formulario')
    return render_template('register.html', title=title, formReg=form_register)


@app.route('/dashboard')
def dashboard():
    title = 'Dashboard'
    return render_template('dashboard.html', title=title)


@app.route('/profile')
def profile():
    title = 'Perfil Usuario'
    id = session['id']
    todo = []
    consulta = select_db_publicacion(id)
    perfil = select_db_perfil(id)
    for item in range(0, len(consulta), 1):
        # for ite in range(0,len(consulta[item]),1):
        comentario = ''
        idc = consulta[item][0]
        comentario = pruebas(idc)
        todo.extend([[consulta[item], comentario]])
    return render_template('profile.html', title=title, perfil=perfil, publicacion=todo, amigo=amigos)


@app.route('/articulos')
def listar_articulos():
    m= hashlib.md5(b'prueba')
    p= hashlib.md5(b'prueba')
    m.digest()
    p.digest()
    print(m.hexdigest(), p.hexdigest())
    return ''.join([choice(ascii_letters + digits) for i in range(50)])
    # return jsonify({'publicacion': publicaciones})


@app.route('/publicacion/<int:id>')
def deletePub(id):
    delete_pub_db(id)
    return redirect('/profile')


@app.route('/comentario/<int:id>')
def deleteCom(id):
    delete_com_db(id)
    return redirect('/profile')


@app.route('/comentario/<string:descripcion>/<int:id>')
def editCom(descripcion, id):
    update_com_db(descripcion, id)
    return redirect('/profile')


@app.route('/comentario/<int:pubId>/<string:descripcion>')
def insertCom(pubId, descripcion):
    usuId = session['id']
    insert_com_db(usuId, pubId, descripcion)
    return redirect('/profile')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


 # Establecer el tiempo de caducidad de la caché de archivos estáticos
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/upload', methods=['POST', 'GET'])  # agregar una ruta
def upload():
    if request.method == 'POST':

        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Verifique el tipo de imagen cargada, solo png, PNG, jpg, JPG, bmp"})
        
        basepath = os.path.join(app.root_path, 'static/') 
        filname = f.filename
        fname = f.filename.split('.', 1)[0]
        nrand = ''.join([choice(ascii_letters + digits) for i in range(50)])
        if (len(select_perfil_db(nrand,0)) > 0 ):
            nrand = ''.join([choice(ascii_letters + digits) for i in range(50)])
        flnm = filname.replace(fname,nrand)

        upload_path = os.path.join(basepath, 'images', secure_filename(flnm))
        f.save(upload_path)

        perfil_db(session['id'],'./static/images/', flnm)

    return redirect('/profile')

@app.route('/uploadP', methods=['POST', 'GET'])  # agregar una ruta
def uploadP():
    if request.method == 'POST':

        f = request.files['fileP']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Verifique el tipo de imagen cargada, solo png, PNG, jpg, JPG, bmp"})
        
        basepath = os.path.join(app.root_path, 'static/') 
        filname = f.filename
        fname = f.filename.split('.', 1)[0]
        nrand = ''.join([choice(ascii_letters + digits) for i in range(50)])
        if (len(select_perfil_db(nrand,0)) > 0 ):
            nrand = ''.join([choice(ascii_letters + digits) for i in range(50)])
        flnm = filname.replace(fname,nrand)

        upload_path = os.path.join(basepath, 'images', secure_filename(flnm))
        f.save(upload_path)

        img_perfil_db(session['id'],'./static/images/', flnm)

    return redirect('/profile')