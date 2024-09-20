from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import datetime
from query import obtenerUsuarios, check_credentials, validarLogin, login_required, lista_miembros, lista_genero

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
app = Flask(__name__, static_folder='static', template_folder='template')

@app.route('/login', methods = ['POST', 'GET'])
def login():     
    error = None
    if request.method == "POST":
        identificacion = request.form['identificacion']
        contrasena = request.form['contrasena']
        print(identificacion, contrasena)
        #LLAMADO A LA FUNCION VALIDARLOGIN
        return validarLogin(identificacion, contrasena)
    check_credentials(0,0)
    return render_template('login.html')

#LLAMADO AL TEMPLATE ADMINISTRADOR
@app.route('/administrator')
@login_required
def administrator():
    return render_template('Administrator/administrator.html')

#LLAMADO AL TEMPLATE MIEMBRO
@app.route('/profile-member')
@login_required
def profile_member():
    return render_template('member/profile.html')

#LLAMADO VISTA GESTION DE USUARIOS
@app.route('/users-manage')
@login_required
def manage_users():
    return render_template('Administrator/manage_users.html')

#VISTA LISTADO DE MIEMBROS
@app.route('/list-members', methods = ['POST', 'GET'])
@login_required
def list_members():
    miembros_gym = lista_miembros()
    return render_template('Administrator/list_members.html', list_miembros = miembros_gym)

#ANADIR USUARIOS
# @app.route('/add-users', method=['POST', 'GET'])
# def add_users():
#     if request.method == 'POST':
#         cedula = request.form['identificacion']
#         nombre = request.form['nombre']
#         apellido = request.form['apellido']
#         edad = request.form['edad']
#         correo = request.form['correo']
#         telefono = request.form['telefono']
#         genero = request.form['genero']
#         plan_trabajo = request.form['plan_trabajo']
#         rol = request.form['rol']
#         contrasena = request.form['contrasena']
    
#     return render_template('Administrator/add_users.html')

if __name__ =='__main__':
    app.run(port =4000, debug =True)