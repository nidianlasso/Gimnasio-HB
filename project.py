from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
from flask_mysqldb import MySQL
from datetime import datetime
from query import (validarLogin, login_required_admin, login_required_member,login_required_coach, login_required_receptionist,
                    lista_miembros,lista_genero, plan_trabajo_lista, lista_roles, cant_miembros, cant_entrenadores,
                      conteo_clases_reservadas, add_user, search_users, assig_membreships, list_membreship,
                      guardar_membresia, status_membreship, actualizar_membresia, lista_maquinas, search_machine, access_users,
                      guardar_acceso, obtener_tipo_acceso, cambiar_estado_acceso, asignar_entrenador)

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


#LLAMADO AL TEMPLATE ENTRENADOR
@app.route('/profile-coach')
@login_required_coach
def profile_coach():
    return render_template('coach/profile.html')

@app.route('/profile-receptionist', methods=['GET', 'POST'])
@login_required_receptionist
def profile_receptionist():
    return render_template('receptionist/profile.html')  # Asegúrate de que resultados tenga un valor




#LLAMADO VISTA GESTION DE USUARIOS
@app.route('/users-manage')
@login_required_admin
def manage_users():
    datosGenero = lista_genero()
    planes_trabajo = plan_trabajo_lista()
    roles = lista_roles()
    membresias = list_membreship()
    estado_membresia = status_membreship()
    return render_template('Administrator/manage_users.html',  listaGeneros=datosGenero, planes_trabajo=planes_trabajo, roles=roles, membresias = membresias, estado_membresia = estado_membresia)

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
        #print(f"Identificación: {cedula}, Nombre: {nombre}, Apellido: {apellido}, Edad: {edad}, Correo: {correo}, Teléfono: {telefono}, Género: {genero}, Plan de trabajo: {plan_trabajo}, Rol: {rol}, Contraseña: {contrasena}")
        if add_user(cedula, nombre, apellido, edad, correo, telefono, genero, plan_trabajo, rol, contrasena):
            flash('Registro exitoso!', 'success')
        else:
            flash('Error al registrar el usuario.', 'error')
    return manage_users()
    

@app.route('/search-users', methods=['POST'])
@login_required_admin
def search_users_name():
    if request.method == 'POST':
        # nombre = request.form['nombre']
        palabra_ingresada = request.json
        palabra_ingresada = palabra_ingresada.get('identificacion')
        print(palabra_ingresada, "extraccion de datos")
        resultados = search_users(palabra_ingresada)   
        print(resultados, "estas son las busquedas")
    return jsonify(resultados)

@app.route('/assign_membreship', methods=['POST','GET'])
@login_required_admin        
def assign_membreship():
    asignacion = assig_membreships()
    return jsonify(asignacion)

@app.route('/save_membreship', methods=['POST'])
@login_required_admin
def save_membreship():
    if request.method == 'POST':
        usuario_id = request.form['usuarioId']  # Asegúrate de que este nombre sea correcto
        tipo_membresia = request.form['tipoMembresia']
        fecha_inicio = request.form['fechaInicio']
        fecha_fin = request.form['fechaFin']
        estado_membresia = request.form['estadoMembresia']
        print("Datos a guardar:", usuario_id, tipo_membresia, fecha_inicio, fecha_fin, estado_membresia)  # Para depuración
        if guardar_membresia(usuario_id, tipo_membresia, fecha_inicio, fecha_fin, estado_membresia):
            flash('Registro exitoso!', 'success')
        else:
            flash('Error al registrar el usuario.', 'error')
    return manage_users()


@app.route('/update_membreship', methods=['POST'])
@login_required_admin
def update_membreship():
    if request.method == 'POST':
        # usuario_id = request.form.get('id_user_update')
        membresia_usuario = request.form.get('id_membresia_usuario')
        tipo_membresia = request.form.get('tipoMembresia')
        fecha_inicio = request.form.get('fechaInicio')
        fecha_fin = request.form.get('fechaFin')
        estado = request.form.get('estadoMembresia')
        print("DATOS QUE SE VAN A ACTUALIZAR EN LA BD")
        print(membresia_usuario, tipo_membresia, fecha_inicio, fecha_fin, estado)
        if actualizar_membresia(tipo_membresia, fecha_inicio, fecha_fin, estado, membresia_usuario):
            flash('Membresía actualizada exitosamente.', 'success')
        else:
            flash('Hubo un error al actualizar la membresía.', 'danger')

    return redirect(url_for('manage_users'))

#GESTION DE LAS MAQUINAS
@app.route('/manage-machine')
@login_required_admin
def manage_machine():
    return render_template('Administrator/manage_machine.html')

@app.route('/list-machine', methods = ['POST', 'GET'])
@login_required_admin
def list_machine():
    maquinas_gym = lista_maquinas()
    return jsonify(maquinas_gym)

@app.route('/search-machine', methods=['POST'])
@login_required_admin
def search_machine_name():
    if request.method == 'POST':
        # nombre = request.form['nombre']
        palabra_ingresada = request.json
        palabra_ingresada = palabra_ingresada.get('identificacion')
        print(palabra_ingresada, "extraccion de datos")
        resultados = search_machine(palabra_ingresada)   
        print(resultados, "estas son las busquedas")
    return jsonify(resultados)

#REGISTRAR LOS ACCESOS
@app.route('/registrar-ingreso', methods=['POST'])
def registrar_ingreso():
    cedula = request.json.get('cedula')
    resultado = access_users(cedula)

    if resultado:
        usuario = resultado[0]  # Obtener la primera tupla
        id_usuario = usuario[0]  # Esto es el id del usuario
        # Retorna la información del usuario y pero también espera la información del acceso
        return jsonify({
            'id_usuario': id_usuario,
            'nombre': usuario[1],
            'apellido': usuario[2],
            'rol': usuario[3]
        }), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/guardar-acceso', methods=['POST'])
def guardar_acceso_route():
    data = request.json
    fecha = data.get('fecha')
    duracion = data.get('duracion')
    tipo_acceso = data.get('tipo_acceso')
    id_usuario = data.get('id_usuario')

    if guardar_acceso(fecha, duracion, tipo_acceso, id_usuario):
        return jsonify({'message': 'Acceso registrado exitosamente'}), 201
    else:
        return jsonify({'error': 'Error al registrar el acceso'}), 500

@app.route('/obtener-acceso', methods=['GET'])
def obtener_acceso():
    id_usuario_str = request.args.get('id_usuario')
    
    if not id_usuario_str:
        return jsonify({'error': 'ID de usuario es requerido'}), 400
    
    try:
        id_usuario = int(id_usuario_str)  # Intenta convertir a entero
    except ValueError:
        return jsonify({'error': 'ID de usuario debe ser un número válido'}), 400

    # Continúa con la lógica para obtener acceso
    acceso = obtener_tipo_acceso(id_usuario)
    
    if acceso is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    return jsonify({'tipo_acceso': acceso}), 200


@app.route('/cambiar-estado-acceso', methods=['POST'])
def route_cambiar_estado_acceso():
    data = request.json
    id_usuario = data.get('id_usuario')

    resultado = cambiar_estado_acceso(id_usuario)

    if 'error' in resultado:
        return jsonify(resultado), 404

    return jsonify(resultado), 200

#ASIGNAR ENTRENADOR
@app.route('/assign-coach', methods=['POST', 'GET'])
def assign_coach_route():
    asignacion = asignar_entrenador()
    print("datos para asignar entrenador")
    print(asignacion)
    return jsonify(asignacion)

# @app.route('/save-assign-coach', methods=['POST'])
# def save_assign_coach():
#     if request.method == 'POST':
#         usuario_id = request.form['usuarioId']  # Asegúrate de que este nombre sea correcto
#         tipo_membresia = request.form['tipoMembresia']
#         fecha_inicio = request.form['fechaInicio']
#         fecha_fin = request.form['fechaFin']
#         estado_membresia = request.form['estadoMembresia']
#         print("Datos a guardar:", usuario_id, tipo_membresia, fecha_inicio, fecha_fin, estado_membresia)  # Para depuración
#         if guardar_membresia(usuario_id, tipo_membresia, fecha_inicio, fecha_fin, estado_membresia):
#             flash('Registro exitoso!', 'success')
#         else:
#             flash('Error al registrar el usuario.', 'error')
#     return manage_users()


if __name__ =='__main__':
    app.run(port =4000, debug =True)