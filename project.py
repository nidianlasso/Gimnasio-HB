from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from query import validarLogin, login_required_admin, login_required_member, lista_miembros, lista_genero, plan_trabajo_lista, lista_roles, cant_miembros, cant_entrenadores, conteo_clases_reservadas, add_user

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
app = Flask(__name__, static_folder='static', template_folder='template')
#KEY SECRET
app.secret_key = '20202578145'
#--KEY SECRET

@app.route('/login', methods = ['POST', 'GET'])
def login(): 
    #se envia el templete de donde se van a obtener las cookies
    resp = make_response(render_template('login.html'))
    #se manipula la cookie que llega y se elimina
    resp.set_cookie('identificacion', '', max_age=0)   
    error = None
    if request.method == "POST":
        identificacion = request.form['identificacion']
        contrasena = request.form['contrasena']
        print(identificacion, contrasena)
        #LLAMADO A LA FUNCION VALIDARLOGIN
        return validarLogin(identificacion, contrasena)
    return resp

#LLAMADO AL TEMPLATE ADMINISTRADOR
@app.route('/administrator')
@login_required_admin
def administrator():
    listado_miembros = cant_miembros()
    listado_entrenadores = cant_entrenadores()
    conteo_clases = conteo_clases_reservadas()
    return render_template('Administrator/administrator.html', lista_miembros = listado_miembros, cant_entrenadores = listado_entrenadores, conteo_reserva = conteo_clases)

#LLAMADO AL TEMPLATE MIEMBRO
@app.route('/profile-member')
@login_required_member
def profile_member():
    return render_template('member/profile.html')

#LLAMADO VISTA GESTION DE USUARIOS
@app.route('/users-manage')
@login_required_admin
def manage_users():
    return render_template('Administrator/manage_users.html')

#VISTA LISTADO DE MIEMBROS
# @app.route('/list-members', methods = ['POST', 'GET'])
# @login_required_admin
# def list_members():
    
#     miembros_gym = lista_miembros()
#     return render_template('Administrator/list_members.html', list_miembros = miembros_gym)


#API VISTA LISTADO DE MIEMBROS
@app.route('/list-members', methods = ['POST', 'GET'])
@login_required_admin
def list_members():
    
    miembros_gym = lista_miembros()
    return jsonify(miembros_gym)


#ANADIR USUARIOS
@app.route('/add-users', methods=['POST', 'GET'])
@login_required_admin
def add_users():
    if request.method == 'POST':
        cedula = request.form['identificacion']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        correo = request.form['correo']
        telefono = request.form['telefono']
        genero = request.form['genero']
        plan_trabajo = request.form['plan_trab']
        rol = request.form['rol']
        contrasena = request.form['contrasena']
        
        # Depurar: imprimir los valores que recibes del formulario
        print("Valores recibidos del formulario:")
        print(f"Identificación: {cedula}, Nombre: {nombre}, Apellido: {apellido}, Edad: {edad}, Correo: {correo}, Teléfono: {telefono}, Género: {genero}, Plan de trabajo: {plan_trabajo}, Rol: {rol}, Contraseña: {contrasena}")
        
        if add_user(cedula, nombre, apellido, edad, correo, telefono, genero, plan_trabajo, rol, contrasena):
            flash('Registro exitoso!', 'success')  # Mensaje de éxito
        else:
            flash('Error al registrar el usuario.', 'error')  # Mensaje de error
        
    datosGenero = lista_genero()
    planes_trabajo = plan_trabajo_lista()
    roles = lista_roles()
    return render_template('Administrator/add_users.html', listaGeneros=datosGenero, planes_trabajo=planes_trabajo, roles=roles)

if __name__ =='__main__':
    app.run(port =4000, debug =True)