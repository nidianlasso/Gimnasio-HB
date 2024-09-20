from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import datetime
from query import obtenerUsuarios, check_credentials, validarLogin, lista_miembros

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
def administrator():
    return render_template('Administrator/administrator.html')

#LLAMADO AL TEMPLATE MIEMBRO
@app.route('/profile-member')
def profile_member():
    return render_template('member/profile.html')

#LLAMADO VISTA GESTION DE USUARIOS
@app.route('/users-manage')
def manage_users():
    return render_template('Administrator/manage_users.html')

#VISTA LISTADO DE MIEMBROS
@app.route('/list-members', methods = ['POST', 'GET'])
def list_members():
    miembros_gym = lista_miembros()
    return render_template('Administrator/list_members.html', list_miembros = miembros_gym)

if __name__ =='__main__':
    app.run(port =4000, debug =True)