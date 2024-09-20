from flask_mysqldb import MySQL
import pymysql
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

def validarLogin(identificacion, contrasena):
    info_user = check_credentials(identificacion, contrasena)
    if info_user:
        rol = info_user[0]
        resp = make_response()
        resp.set_cookie('identificacion', identificacion)

        if rol =="Administrador":
            return make_response(redirect(url_for('administrator')))
        elif rol =="Miembro":
            return make_response(redirect(url_for('profile_member')))
    
    error = "Credenciales incorrectas. Intente de nuevo."
    return render_template('login.html', error=error)


#---VERIFICAR LAS CREDENCIALES DE LOS USUARIOS
def check_credentials(identificacion, contrasena):
    cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE identificacion = %s AND contrasena = %s", (identificacion, contrasena))
    info_user = cursor.fetchone()
    print("ESTA ES LA CONSULTA DEL MIEMBRO")
    print(info_user)
    return info_user
#---VERIFICAR LAS CREDENCIALES DE LOS USUARIOS