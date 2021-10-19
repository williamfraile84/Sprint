import sqlite3

def get_db():

    try:
        con = sqlite3.connect('SocialMeliponaBeecheii.db')
        return con
    except sqlite3.Error as e:
        # print("An error occurred:", e.args[0])
        return ("An error occurred:", e.args[0])

def select_db(usuario):
    strsql = "SELECT usuario, contraseña  FROM usuarios where usuario = ?;"
    con = get_db()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,[usuario])

    consultaRespuesta = cursorObj.fetchall()
    return consultaRespuesta

def insert_db(nombre,usuario,email,contraseña,fechaNacimiento,sexo):
    try:
        strsql = "INSERT INTO usuarios (nombre,usuario,email,contraseña,fechaNacimiento,sexo) VALUES (?,?,?,?,?,?);"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute(strsql,(nombre,usuario,email,contraseña,fechaNacimiento,sexo))
        con.commit()
        # print('Usuario Agregado+++++++++++++++++++++++++++++++++++++')
        return 'Usuario Agregado'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al insertar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()

