import sqlite3

def get_db():

    try:
        con = sqlite3.connect('SocialMeliponaBeecheii.db')
        return con
    except sqlite3.Error as e:
        # print("An error occurred:", e.args[0])
        return ("An error occurred:", e.args[0])

def select_db(usuario):
    strsql = "SELECT id, usuario, contraseña  FROM usuarios where usuario = ?;"
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
        cursorObj.execute("PRAGMA foreign_keys = ON")
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

def select_db_publicacion(id_usuario):
    strsql = """
select p.id, u.id as usuarioId, ip.path, ip.nombre_imagen, u.nombre, p.fecha_publicacion, p.path, p.imagen_publicacion from usuarios as u
left join imagen_perfil as ip on u.id = ip.usuario_id
left join publicaciones as p on u.id = p.usuario_id
where u.id =?
    """
    con = get_db()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,[id_usuario])

    consultaRespuesta = cursorObj.fetchall()
    return consultaRespuesta


def pruebas(id):
    strsql = """
    select  p.id, c.id,  ip.path,  ip.nombre_imagen,  u.nombre,  c.publicacion_id,  c.descripcion 
from comentarios as c 
inner join publicaciones as p on c.publicacion_id = p.id 
inner join imagen_perfil as ip on c.usuario_id = ip.usuario_id
inner join usuarios as u on u.id = ip.usuario_id
where p.id=?
    """
    con = get_db()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,[id])

    consultaRespuesta = cursorObj.fetchall()
    return consultaRespuesta

def delete_pub_db(idPub):
    try:
        strsql = "DELETE FROM publicaciones WHERE id = ? ;"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute("PRAGMA foreign_keys = ON")
        cursorObj.execute(strsql,[idPub])
        con.commit()
        # print('Usuario Agregado+++++++++++++++++++++++++++++++++++++')
        return 'Publicacion Eliminada'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al eliminar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()

def delete_com_db(idCom):
    try:
        strsql = "DELETE FROM comentarios WHERE id = ? ;"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute("PRAGMA foreign_keys = ON")
        cursorObj.execute(strsql,[idCom])
        con.commit()
        # print('Usuario Agregado+++++++++++++++++++++++++++++++++++++')
        return 'Comentario Eliminado'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al eliminar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()

def update_com_db(descripcion,idCom):
    try:
        strsql = "UPDATE comentarios SET descripcion = ? WHERE id = ? ;"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute("PRAGMA foreign_keys = ON")
        cursorObj.execute(strsql,[descripcion,idCom])
        con.commit()
        # print('Usuario Agregado+++++++++++++++++++++++++++++++++++++')
        return 'Comentario Actualizado'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al eliminar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()

def insert_com_db(usuId,pubId,descripcion):
    try:
        strsql = "INSERT INTO comentarios (usuario_id,publicacion_id,descripcion) VALUES (?,?,?);"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute("PRAGMA foreign_keys = ON")
        cursorObj.execute(strsql,[usuId,pubId,descripcion])
        con.commit()
        # print('Usuario Agregado+++++++++++++++++++++++++++++++++++++')
        return 'Comentario Insertado'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al eliminar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()

def select_perfil_db(usuario_id,tipo):
    if tipo == 1:
        strsql = "SELECT usuario_id,path,nombre_img_Portada FROM perfiles WHERE usuario_id=?;"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute(strsql,[usuario_id])
        consultaRespuesta = cursorObj.fetchall()
        print(consultaRespuesta)
        return consultaRespuesta
    else:
        strsql = "SELECT usuario_id,path,nombre_img_Portada FROM perfiles where nombre_img_Portada=?;"
        con = get_db()
        cursorObj = con.cursor()
        cursorObj.execute(strsql,[usuario_id])
        consultaRespuesta = cursorObj.fetchall()
        print(consultaRespuesta)
        return consultaRespuesta

def perfil_db(usuario_id,path,nombre_img_Portada):
    try:
        consultaRespuesta = select_perfil_db(usuario_id,1)

        if len(consultaRespuesta) > 0 :
            strsql = "UPDATE perfiles SET nombre_img_Portada = ?  WHERE usuario_id = ?"
            con = get_db()
            cursorObj = con.cursor()
            cursorObj.execute("PRAGMA foreign_keys = ON")
            cursorObj.execute(strsql,[nombre_img_Portada,usuario_id])
            con.commit()
            return 'Portada actualizado'
        else:
            strsql = "INSERT INTO perfiles (usuario_id,path,nombre_img_Portada) VALUES (?,?,?);"
            con = get_db()
            cursorObj = con.cursor()
            cursorObj.execute("PRAGMA foreign_keys = ON")
            cursorObj.execute(strsql,[usuario_id,path,nombre_img_Portada])
            con.commit()
            return 'Portada Insertado'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al eliminar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()

def select_img_perfil_db(usuario_id):
    strsql = "SELECT id,path,nombre_imagen,usuario_id FROM imagen_perfil where usuario_id =?;"
    con = get_db()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,[usuario_id])
    consultaRespuesta = cursorObj.fetchall()
    print(consultaRespuesta)
    return consultaRespuesta

def img_perfil_db(usuario_id,path,nombre_img_Portada):
    try:
        consultaRespuesta = select_img_perfil_db(usuario_id)

        if len(consultaRespuesta) > 0 :
            strsql = "UPDATE imagen_perfil SET nombre_imagen = ? WHERE usuario_id = ?;"
            con = get_db()
            cursorObj = con.cursor()
            cursorObj.execute("PRAGMA foreign_keys = ON")
            cursorObj.execute(strsql,[nombre_img_Portada,usuario_id])
            con.commit()
            return 'Perfil actualizado'
        else:
            strsql = "INSERT INTO imagen_perfil (path,nombre_imagen,usuario_id) VALUES (?,?,?);"
            con = get_db()
            cursorObj = con.cursor()
            cursorObj.execute("PRAGMA foreign_keys = ON")
            cursorObj.execute(strsql,[path,nombre_img_Portada,usuario_id])
            con.commit()
            return 'Perfil Insertado'

    except sqlite3.Error as e:
        con.rollback()
        print("An error occurred:", e.args[0])
        print('Error al eliminar datos------------------------------')
        return ("An error occurred:", e.args[0])
    finally:
        print('Cerrando Conexion **********************************')
        con.close()


def select_db_perfil(id_usuario):
    strsql = """
select u.id, u.nombre, ip.path, ip.nombre_imagen, pe.path, pe.nombre_img_Portada from usuarios as u
left join imagen_perfil as ip on ip.usuario_id= u.id
left join perfiles as pe on pe.usuario_id = u.id
where u.id =?
    """
    con = get_db()
    cursorObj = con.cursor()
    cursorObj.execute(strsql,[id_usuario])

    consultaRespuesta = cursorObj.fetchall()
    return consultaRespuesta