from flask_mysqldb import MySQL
import pymysql
from functools import wraps
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
import datetime

app = Flask(__name__, static_folder='static', template_folder='template')
# Configura la conexión a la base de datos MySQL
connection = pymysql.connect(host="localhost", user="root", passwd="12345", database="bd_gimnasio2")
cursor = connection.cursor()

def obtenerUsuarios():
    cursor.execute("SELECT * FROM bd_gimnasio2.usuario")
    rows = cursor.fetchall()
    cursor.close()  # Asegúrate de cerrar el cursor
    return rows

from flask import render_template, redirect, url_for, request, make_response

# Función para validar el login del usuario
def validarLogin(identificacion, contrasena):
    info_user = check_credentials(identificacion, contrasena)
    if info_user:
        rol = info_user[0]  # Obtener el rol del usuario
        resp = make_response()  # Crear la respuesta base
        
        # Establecer la cookie de 'identificacion' por 24 horas (86400 segundos)
        resp.set_cookie('identificacion', identificacion, max_age=86400)  

        # Redirigir según el rol del usuario
        if rol == "Administrador":
            resp = make_response(redirect(url_for('administrator')))
        elif rol == "Miembro":
            resp = make_response(redirect(url_for('profile_member')))
        
        # Devolver la respuesta con la cookie establecida
        return resp  

    # Si las credenciales son incorrectas, mostrar error
    error = "Credenciales incorrectas. Intente de nuevo."
    return render_template('login.html', error=error)

# Función para verificar las credenciales en la base de datos
def check_credentials(identificacion, contrasena):
    query = """
        SELECT r.nombre 
        FROM bd_gimnasio2.usuario u 
        INNER JOIN rol r ON u.id_rol = r.id_rol 
        WHERE identificacion = %s AND contrasena = %s
    """
    cursor.execute(query, (identificacion, contrasena))
    info_user = cursor.fetchone()
    
    print("Resultado de la consulta para el login del usuario:")
    print(info_user)  # Verificación del resultado de la consulta para depurar
    return info_user

#--GUARDAR LA COKKIE
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si la cookie 'identificacion' está presente
        identificacion = request.cookies.get('identificacion')
        
        if not identificacion:  # Si no hay cookie, redirigir al login
            print("Usuario no autenticado. Redirigiendo al login.")
            return redirect(url_for('login'))
        
        print(f"Usuario autenticado con identificación: {identificacion}")
        # Si la cookie existe, proceder a la función protegida
        return f(*args, **kwargs)
    return decorated_function

#--GUARDAR LA COKKIE


#OBTENER EL LISTADO DE MIEMBROS
def lista_miembros():
    cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, u.edad, u.correo, u.telefono FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE r.nombre = 'Miembro'")
    listado_miembros = cursor.fetchall()
    return listado_miembros
#OBTENER EL LISTADO DE MIEMBROS

#--LISTADO DE GENERO
def lista_genero():
    cursor.execute("SELECT * FROM genero")
    result_gender= cursor.fetchall()
    return result_gender
#--LISTADO DE GENERO

#--AGREGAR USUARIO

#--AGREGAR USUARIO