from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response, send_file
from flask_mysqldb import MySQL
from datetime import datetime, timedelta, date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from werkzeug.security import generate_password_hash, check_password_hash
from query import (
    validarLogin, check_credentials,horario_empleado, login_required_admin, login_required_member,obtener_usuarios_con_membresia, guardar_membresia, login_required_coach, login_required_receptionist,
    lista_miembros, lista_genero, plan_trabajo_lista, lista_roles, cant_miembros, cant_entrenadores,
    conteo_clases_reservadas, add_user, search_users, assig_membreships, list_membreship, obtener_membrehip_user,
    status_membreship, actualizar_membresia, lista_maquinas, listado_empleados, lista_proveedores, search_machine, access_users,
    guardar_acceso, cambiar_estado_acceso_db, obtener_plan_trabajo, obtener_membrehip_user,
    save_class_to_db, list_class, delete_class, obtener_reservas_maquinas, obtener_maquinas_disponibles, consultar_reservas_de_hoy, cant_maquinas,
    cant_proveedores, cant_empleados, obtener_maquinas_disponibles_para_reserva, existe_reserva_en_bloque, registrar_reserva,
    obtener_id_membresia_usuario, consultar_bloques_contiguos, registrar_pago_nomina, obtener_id_usuario_por_identificacion, insertar_proveedor,
    eliminar_proveedor_id, actualizar_proveedor, obtener_proveedor_por_id, obtener_clases_disponibles, obtener_id_membresia_usuario_activa, insertar_reserva_clase,
    existe_reserva, obtener_reservas_usuario, obtener_clase_por_id, cancelar_reserva_en_bd, obtener_id_clase_por_nombre, obtener_clientes_sin_avance_hoy, insertar_progreso,
    existe_avance_hoy, obtener_historial_avances, maquinas_sin_disponibles, insertar_revision,
    insert_revision_sql, insert_observacion_sql, insertar_revision, reports_machine, actualizar_estado_revision, insertar_observacion, obtener_revision, obtener_observaciones, obtener_revisiones_pendientes,
    actualizar_observacion_tecnico, lista_tecnicos, actualizar_usuario, datos_usuario,
    actualizar_datos_usuario, hash_password, obtener_rutinas_por_plan, insertar_rutina, insertar_zona_cuerpo, obtener_cliente_por_plan, finalizar_acceso,
    consultar_acceso_usuario, obtener_miembros_por_plan, obtener_entrenador, asignar_supervision, asignar_entrenador)

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
app = Flask(__name__, static_folder='static', template_folder='template')
#KEY SECRET
app.secret_key = '20202578145'
#--KEY SECRET

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    resp = make_response(render_template('login.html'))
    resp.set_cookie('identificacion', '', max_age=0)

    if request.method == "POST":
        identificacion = request.form['identificacion']
        contrasena = request.form['contrasena']
        print(">>> Intento de login:", identificacion, contrasena)

        return validarLogin(identificacion, contrasena)

    return resp



#LLAMADO AL TEMPLATE ADMINISTRADOR
@app.route('/administrator')
@login_required_admin
def administrator():
    listado_miembros = cant_miembros()
    listado_entrenadores = cant_entrenadores()
    conteo_clases = conteo_clases_reservadas()
    conteo_maquinas = cant_maquinas()
    conteo_proveedores = cant_proveedores()
    conteo_empleados = cant_empleados()
    return render_template('Administrator/administrator.html', lista_miembros = listado_miembros, cant_entrenadores = listado_entrenadores, conteo_reserva = conteo_clases, conteo_maquinas =conteo_maquinas, conteo_proveedores=conteo_proveedores, cant_empleados=conteo_empleados)

#LLAMADO VISTA GESTION DE USUARIOS
@app.route('/users-manage')
@login_required_admin
def manage_users():
    datosGenero = lista_genero()
    planes_trabajo = plan_trabajo_lista()
    roles = lista_roles()
    membresias = list_membreship()
    estado_membresia = status_membreship()
    horario = horario_empleado()
    return render_template('Administrator/manage_users.html',  listaGeneros=datosGenero, planes_trabajo=planes_trabajo, roles=roles, membresias = membresias, estado_membresia = estado_membresia, horario=horario)

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
        horario = request.form.get('horario')  # ← asegúrate de usar .get()
        contrasena = request.form['contrasena']

        print(f"Llegada de la ID {cedula} *****************")

        if add_user(cedula, nombre, apellido, edad, correo, telefono, genero, plan_trabajo, rol, contrasena, horario):
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

@app.route('/assign_membership', methods=['POST', 'GET'])
@login_required_admin        
def assign_membership():
    asignacion = assig_membreships()
    print(f"Esto llega de la asignación de membresía: {asignacion}")
    return jsonify(asignacion)


@app.route('/save_membreship', methods=['POST'])
@login_required_admin
def save_membreship():
    if request.method == 'POST':
        usuario_id = request.form['usuarioId'] 
        tipo_membresia = request.form['tipoMembresia']
        fecha_inicio = request.form['fechaInicio']
        fecha_fin = request.form['fechaFin']
        estado_membresia = request.form['estadoMembresia']
        print("Datos a guardar:", usuario_id, tipo_membresia, fecha_inicio, fecha_fin, estado_membresia)
        if guardar_membresia(usuario_id, tipo_membresia, fecha_inicio, fecha_fin, estado_membresia):
            flash('Registro exitoso!', 'success')
        else:
            flash('Error al registrar el usuario.', 'error')
    return manage_users()

@app.route('/get_assigned_memberships', methods=['GET'])
@login_required_admin
def get_assigned_memberships():
    data = obtener_usuarios_con_membresia()
    return jsonify(data)

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

#LISTADO DE LAS MAQUINAS CON DISPONIBILIDAD
@app.route('/maquinas', methods=['GET'])
def available_machines_page():
    tipo = request.args.get('tipo')
    if tipo == 'reservadas':
        return jsonify(obtener_reservas_maquinas())
    elif tipo == 'disponibles':
        return jsonify(obtener_maquinas_disponibles())
    elif tipo == 'disponibilidad_horaria':
        return jsonify(obtener_bloques_disponibles())
    else:
        return jsonify({'error': 'Tipo inválido'}), 400


def obtener_bloques_disponibles():
    datos = consultar_reservas_de_hoy()

    maquinas = {}
    for fila in datos:
        id_maquina = fila[0]
        nombre_maquina = fila[1]
        hora_reservada = fila[2]

        if id_maquina not in maquinas:
            maquinas[id_maquina] = {
                "nombre_maquina": nombre_maquina,
                "reservadas": set()
            }

        if hora_reservada:
            if isinstance(hora_reservada, timedelta):
                total_minutes = int(hora_reservada.total_seconds() // 60)
                hora_str = f"{total_minutes // 60:02}:{total_minutes % 60:02}"
            elif isinstance(hora_reservada, datetime):
                hora_str = hora_reservada.strftime('%H:%M')
            else:
                hora_str = hora_reservada.strftime('%H:%M')

            maquinas[id_maquina]["reservadas"].add(hora_str)

    resultado = []

    for id_maquina, datos_maquina in maquinas.items():
        bloques_por_hora = {}

        for i in range(16):  # 06:00 a 21:45
            hora_inicio_bloque = datetime.strptime("06:00", "%H:%M") + timedelta(hours=i)
            hora_key = hora_inicio_bloque.strftime('%H:%M')
            bloques_por_hora[hora_key] = []

            for j in range(4):  # 4 bloques de 15 min
                bloque_inicio = hora_inicio_bloque + timedelta(minutes=15 * j)
                bloque_str = bloque_inicio.strftime('%H:%M')
                estado = "reservado" if bloque_str in datos_maquina["reservadas"] else "disponible"
                bloques_por_hora[hora_key].append({
                    "hora": bloque_str,
                    "estado": estado
                })

        resultado.append({
            "id_maquina": id_maquina,
            "nombre_maquina": datos_maquina["nombre_maquina"],
            "bloques": bloques_por_hora
        })

    return resultado
#**************************RESERVAS DEL USUARIO MAQUINA***********************************************
@app.route('/machine-reservation', methods=['GET'])
def show_machine_reservation_form():
    if 'rol' not in session:
        return redirect('/login')
    return render_template('member/machine_reservation.html', rol=f"perfil-{session['rol']}")

@app.route('/member/disponibilidad', methods=['GET'])
def disponibilidad_para_miembros():
    return jsonify(obtener_bloques_disponibles())


@app.route('/reservar-bloque', methods=['POST'])
def reservar_bloque():
    print(">>> INICIO de reservar_bloque")
    print("ROL en sesión:", session.get('rol'))


    if 'id_usuario' not in session or session.get('rol') != 'miembro':
        return jsonify({'success': False, 'message': 'Acceso no autorizado'}), 403

    datos = request.get_json()
    print(">>> Paso 2: JSON recibido:", datos)

    id_inventario_maquina = datos.get('id_maquina')
    hora_inicio = datos.get('hora')

    if not id_inventario_maquina or not hora_inicio:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400

    #convertir a formato completo HH:MM:SS
    if len(hora_inicio) == 5:
        hora_inicio += ":00"
    print(">>> Hora formateada:", hora_inicio)

    identificacion = session['identificacion']
    id_membresia_usuario = obtener_id_membresia_usuario(identificacion)
    print(">>> ID membresía usuario:", id_membresia_usuario)

    if not id_membresia_usuario:
        return jsonify({'success': False, 'message': 'No se encontró membresía activa asociada al usuario'}), 404

    try:
        hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M:%S")
    except ValueError:
        return jsonify({'success': False, 'message': 'Formato de hora inválido'}), 400

    hora_fin_dt = hora_inicio_dt + timedelta(minutes=15)
    hora_fin_str = hora_fin_dt.strftime('%H:%M:%S')

    if existe_reserva_en_bloque(id_inventario_maquina, hora_inicio):
        print(">>> BLOQUE YA RESERVADO")
        return jsonify({'success': False, 'message': 'Este bloque ya está reservado'}), 409

    if existe_reserva_contigua(id_membresia_usuario, hora_inicio):
        return jsonify({'success': False, 'message': 'No puedes reservar bloques seguidos'}), 409

    resultado = registrar_reserva(id_membresia_usuario, id_inventario_maquina, hora_inicio, hora_fin_str)
    return jsonify(resultado), 201 if resultado['success'] else 500


def existe_reserva_contigua(id_membresia_usuario, hora_inicio):
    resultado = consultar_bloques_contiguos(id_membresia_usuario, hora_inicio)
    return resultado is not None

#*************************************************************************

#RESERVAR CLASES

@app.route('/clases', methods=["GET"])
def listado_clases():
    clases = obtener_clases_disponibles()
    return render_template('member/class_reservation.html', clases=clases)

@app.route("/reservar-clase", methods=["POST"])
def reservar_clase():
    try:
        id_clase = request.form.get("id_clase")
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        id_usuario = session.get("id_usuario")

        if not id_usuario:
            return jsonify({"error": "Usuario no autenticado"}), 401

        id_membresia_usuario = obtener_id_membresia_usuario_activa(id_usuario)

        if not id_membresia_usuario:
            return jsonify({"error": "No tienes una membresía activa"}), 400

        if existe_reserva(id_clase, id_membresia_usuario, fecha, hora):
            return jsonify({"error": "Ya has reservado esta clase"}), 400

        resultado = insertar_reserva_clase(fecha, hora, id_clase, id_membresia_usuario)
        return jsonify({"mensaje": "Reserva realizada con éxito"}), 200

    except Exception as e:
        print("Error en reservar_clase:", e)
        return jsonify({"error": str(e)}), 500

#GESTION DE CLASES RESERVADAS
@app.route('/mis-clases')
def mis_clases():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return "Usuario no autenticado", 401
    reservas = obtener_reservas_usuario(id_usuario)
    return render_template('/member/mis_clases.html', reservas=reservas)

@app.route('/cancelar-reserva', methods=['POST'])
def cancelar_reserva():
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    nombre_clase = request.form.get('nombre_clase')
    id_usuario = session.get('id_usuario')

    if not id_usuario:
        return "No autorizado", 401

    id_membresia_usuario = obtener_id_membresia_usuario_activa(id_usuario)
    if not id_membresia_usuario:
        return "No tienes una membresía activa.", 403

    id_clase = obtener_id_clase_por_nombre(nombre_clase)
    if not id_clase:
        return "Clase no encontrada", 404

    cancelar_reserva_en_bd(id_clase, id_membresia_usuario, fecha, hora)

    flash("Reserva cancelada exitosamente.", "success")
    return redirect(url_for('mis_clases'))


# ENVIAR MAQUINA A REVISION
@app.route('/review-machines', methods=['GET'])
def review_machines():
    asignacion = lista_maquinas()
    return jsonify(asignacion)
#ENVIO DE MAQUINA A REVISION

#LLAMADO AL TEMPLATE MIEMBRO
# @app.route('/profile-member')
# @login_required_member
# def profile_member():
#     identificacion = session.get('identificacion')
#     print(f"Identificación obtenida de la sesión: {identificacion}")
#     if not identificacion :
#         return redirect(url_for('login'))
    
#     if "id_usuario" not in session:
#         return redirect(url_for("login"))

#     id_usuario = session["id_usuario"]
    
#     plan_trabajo = obtener_plan_trabajo(identificacion)
#     membresia_asignada = obtener_membrehip_user(identificacion)
#     miembro = datos_miembro(id_usuario)
#     print(f"Esto llega de los datos del miembro")

#     if not miembro:
#         return "No se encontró el perfil del entrenador o no tiene rol 'Entrenador'", 404


#     return render_template('member/profile.html', plan_trabajo=plan_trabajo, membresia = membresia_asignada, miembro = miembro)

# @app.route("/editar-profile-member", methods=["GET"])
# def edit_profile_member():
#     if "id_usuario" not in session:
#         return redirect(url_for("login"))
    
#     id_usuario = session["id_usuario"]
#     entrenador = datos_miembro(id_usuario)
    
#     if not entrenador:
#         flash("No se encontró el entrenador.", "error")
#         return redirect(url_for("profile_member"))
    
#     return render_template("edit_profile.html", entrenador=entrenador)

# @app.route('/update-profile-member', methods=['POST'])
# def update_profile_member():
#     id_usuario =  session["id_usuario"]
#     nombre = request.form['nombre']
#     apellido = request.form['apellido']
#     identificacion = request.form['identificacion']
#     edad = request.form['edad']
#     correo = request.form['correo']
#     telefono = request.form['telefono']
#     contrasena = request.form.get('contrasena', '').strip()

#     if contrasena:
#         contrasena_hash = hash_password(contrasena)
#     else:
#         contrasena_hash = None

#     actualizar_datos_miembro(id_usuario, nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash)

#     return redirect(url_for('perfil_entrenador'))



#TEMPLETE PRINCIPAL DEL MIEMBRO
@app.route('/inicio')
def index_member():
    identificacion = session.get('identificacion')
    if "rol" not in session:
        return redirect(url_for("login"))
    
    return render_template('member/index.html', rol=session["rol"])

#RESERVAR MÁQUINAS ***********************************************************
# 1. Controlador que retorna las máquinas disponibles en JSON
@app.route('/api/maquinas_disponibles', methods=['GET'])
def api_maquinas_disponibles():
    maquinas = obtener_maquinas_disponibles_para_reserva()
    resultado = [{"id": m[0], "nombre": m[1]} for m in maquinas]
    return jsonify(resultado)



# *************************************************************************

#LLAMADO AL TEMPLATE ENTRENADOR
@app.route('/index-coach')
@login_required_coach
def index_coach():
    return render_template('coach/index.html', carpeta_rol="coach")

@app.route('/index-receptionist', methods=['GET', 'POST'])
@login_required_receptionist
def index_receptionist():
    return render_template('receptionist/index.html', carpeta_rol="receptionist")    

#REGISTRAR LOS ACCESOS
@app.route('/registrar-ingreso', methods=['POST'])
def registrar_ingreso():
    cedula = request.json.get('cedula')
    resultado = access_users(cedula)
    if resultado:
        usuario = resultado[0]
        id_usuario = usuario[0]
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
    tipo_acceso = data.get('tipo_acceso')
    id_usuario = data.get('id_usuario')

    # Validar parámetros obligatorios
    if not id_usuario or not tipo_acceso:
        return jsonify({'error': 'Faltan parámetros (id_usuario o tipo_acceso)'}), 400

    # Guardar acceso (la BD pondrá duracion=00:00:00 automáticamente)
    if guardar_acceso(tipo_acceso, id_usuario):
        return jsonify({'message': 'Acceso registrado exitosamente'}), 201
    else:
        return jsonify({'error': 'Error al registrar el acceso'}), 500


@app.route('/finalizar-acceso', methods=['POST'])
def finalizar_acceso():
    data = request.json
    id_usuario = data.get('id_usuario')

    if not id_usuario:
        return jsonify({'error': 'Falta el id_usuario'}), 400

    resultado = finalizar_acceso(id_usuario)

    if 'error' in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200


# 🔹 Ruta Flask: recibe petición y usa la función lógica
@app.route('/obtener-acceso', methods=['GET'])
def route_obtener_acceso():
    id_usuario = request.args.get('id_usuario')

    if not id_usuario:
        return jsonify({'error': 'id_usuario es requerido'}), 400

    resultado = consultar_acceso_usuario(id_usuario)

    if 'error' in resultado:
        return jsonify(resultado), 500

    return jsonify(resultado), 200

@app.route('/cambiar-estado-acceso', methods=['POST'])
def cambiar_estado_acceso():
    try:
        data = request.json
        id_usuario = data.get('id_usuario')

        if not id_usuario:
            return jsonify({'error': 'id_usuario es requerido'}), 400

        resultado = cambiar_estado_acceso_db(id_usuario)

        if 'error' in resultado:
            return jsonify(resultado), 404

        return jsonify(resultado), 200

    except Exception as e:
        print("Error en cambiar_estado_acceso:", e)
        return jsonify({'error': f'Error al cambiar el estado del acceso: {str(e)}'}), 500


@app.route('/asignar_supervision/<int:id_entrenador>', methods=['POST'])
def asignar_supervision_automatica(id_entrenador):
    fecha = request.form.get("fecha")  # O la fecha actual si prefieres

    # 1. Traer datos del entrenador
    entrenador = obtener_entrenador(id_entrenador)
    if not entrenador:
        return "Entrenador no encontrado", 404

    # 2. Buscar los miembros con el mismo plan
    miembros = obtener_miembros_por_plan(entrenador["id_plan"])

    # 3. Insertar la supervisión para cada miembro
    for m in miembros:
        asignar_supervision(entrenador["id_usuario"], m["id_usuario"], fecha)

    return f"Supervisión asignada para {len(miembros)} miembros con el entrenador {entrenador['id_usuario']}"


#ASIGNAR ENTRENADOR
@app.route('/assign-coach', methods=['POST', 'GET'])
def assign_coach_route():
    try:
        asignacion = asignar_entrenador()
        print("📥 Datos para asignar entrenador:", asignacion)  # 👀 DEBUG
        return jsonify(asignacion), 200
    except Exception as e:
        print("❌ Error en assign_coach_route:", e)
        return jsonify({'error': str(e)}), 500


#MOSTRAR PLAN DE TRABAJO DEL MIEMBRO

#MOSTRAR OPCIONES PARA CLASES
@app.route('/acciones-clase')
def acciones_clase():
    return render_template('Administrator/options_class.html')

#CREACION DE LAS CLASES
@app.route('/create-class', methods=['GET'])
def show_create_class_form():
    return render_template('Administrator/create_class.html')


@app.route('/create-class', methods=['POST'])
def create_class():
    nombre = request.form.get('nombre')
    fecha_inicio = request.form.get('fecha_inicio')
    hora = request.form.get('hora')
    duration = request.form.get('duration')
    print(nombre, fecha_inicio, hora, duration)
    if not all([nombre, fecha_inicio, hora, duration]):
        return jsonify({'success': False, 'message': 'Todos los campos son obligatorios.'}), 400

    result = save_class_to_db(nombre, fecha_inicio, hora, duration)

    if result['success']:
        return render_template('Administrator/create_class.html')
    else:
        return jsonify(result), 500

#Eliminar clase
@app.route('/delete-class', methods=['GET', 'POST'])
def delete_class_admin():
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        result = delete_class(class_id)
        classes = list_class()
        return render_template('Administrator/delete_class.html', clases=classes, clase_delete=result)
    
    classes = list_class()
    return render_template('Administrator/delete_class.html', clases=classes)


@app.route('/formulario-nomina')
def mostrar_formulario_nomina():
    try:
        empleados =  listado_empleados()
        return render_template('Administrator/nomina.html', empleados=empleados)
    except Exception as e:
        print(f"Error al cargar formulario de nómina: {e}")
        flash("Error cargando formulario", "error")
        return redirect(url_for('home'))

@app.route('/insertar-nomina', methods=['POST'])
def insertar_nomina():
    try:
        identificacion = request.form.get('identificacion').strip()
        id_usuario = obtener_id_usuario_por_identificacion(identificacion)

        if not id_usuario:
            print(f"No se encontró usuario con identificación {identificacion}")
        else:
            print(f"Este es el id_usuario que llega: {id_usuario} !!!!!!!***************")

        # Conversión segura
        id_usuario = int(request.form.get('identificacion', 0))
        nombre =request.form.get('nombre', '')
        apellido =request.form.get('apellido', '')
        fecha_generacion = request.form.get('fecha_pago', '')
        salario_base = float(request.form.get('salario', 0) or 0)
        auxilio_transporte = float(request.form.get('auxilio', 0) or 0)
        aporte_salud = float(request.form.get('salud', 0) or 0)
        aporte_pension = float(request.form.get('pension', 0) or 0)
        total_devengado = float(request.form.get('total_devengado', 0) or 0)
        total_deducciones = float(request.form.get('total_deducciones', 0) or 0)
        liquido_a_recibir = float(request.form.get('liquido', 0) or 0)

        # dats de nomina en BD
        datos = (
            id_usuario, fecha_generacion, salario_base,
            auxilio_transporte, aporte_salud, aporte_pension,
            total_devengado, total_deducciones, liquido_a_recibir
        )

        exito = registrar_pago_nomina(datos)

        if exito:
            carpeta_pdfs = os.path.join(os.getcwd(), "static", "pdfs")
            os.makedirs(carpeta_pdfs, exist_ok=True)
            ruta_pdf = os.path.join(carpeta_pdfs, f"nomina_{identificacion}.pdf")
            generar_pdf(
                ruta_pdf,
                identificacion=identificacion,
                nombre=nombre,
                apellido=apellido,
                fecha=fecha_generacion,
                salario=salario_base,
                auxilio=auxilio_transporte,
                salud=aporte_salud,
                pension=aporte_pension,
                devengado=total_devengado,
                deducciones=total_deducciones,
                liquido=liquido_a_recibir
            )

            return send_file(ruta_pdf, as_attachment=True)


        else:
            return "Error al registrar en la base de datos", 500

    except Exception as e:
        print("Error en /insertar-nomina:", e)
        return "Error al procesar la solicitud", 500


def generar_pdf(ruta, identificacion,nombre, apellido, fecha, salario, auxilio, salud, pension, devengado, deducciones, liquido):
    doc = SimpleDocTemplate(ruta, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []

    # Título principal
    titulo = Paragraph("<b><font size=16 color='#003366'>COMPROBANTE DE NÓMINA</font></b>", estilos["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    # Datos de la Empresa
    empresa_data = [
        ['EMPRESA', ''],
        ['Nombre:', 'Gimnasio La Candelaria'],
        ['Dirección:', 'Cl. 68 Sur # 47 - 10, Cdad. Bolívar, Bogotá'],
    ]
    empresa_table = Table(empresa_data, colWidths=[180, 300])
    empresa_table.setStyle(TableStyle([
        ('SPAN', (0,0), (-1,0)),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e6f2ff')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#003366')),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,1), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    elementos.append(empresa_table)
    elementos.append(Spacer(1, 16))

    # Datos del Trabajador
    trabajador_data = [
        ['TRABAJADOR/A', ''],
        ['Empleado/a:', (nombre), (apellido)],
        ['Identificación:', str(identificacion)],
    ]
    trabajador_table = Table(trabajador_data, colWidths=[160, 80, 100, 100])
    trabajador_table.setStyle(TableStyle([
        ('SPAN', (0,0), (-1,0)),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#fff2cc')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#7f6000')),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,1), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    elementos.append(trabajador_table)
    elementos.append(Spacer(1, 16))

    # Devengos
    devengos_data = [
        ['Devengos', 'Cantidad', 'Precio ($)', 'Total ($)'],
        ['Salario base', '30 días', f"{salario:,.0f}", f"{salario * 30:,.0f}"],
        ['Auxilio de transporte', '', f"{auxilio:,.0f}", f"{auxilio:,.0f}"],
        ['Total', '', '', f"{devengado:,.0f}"],
    ]
    devengos_table = Table(devengos_data, colWidths=[160, 80, 100, 100])
    devengos_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d9ead3')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#274e13')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (1,1), (-1,-2), 'CENTER'),
        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
    ]))
    elementos.append(devengos_table)
    elementos.append(Spacer(1, 16))

    # Deducciones
    deducciones_data = [
        ['Deducciones', 'Cantidad', 'Porcentaje', 'Total ($)'],
        ['Aporte a la salud', '', '4%', f"{salud:,.0f}"],
        ['Aporte a la pensión', '', '4%', f"{pension:,.0f}"],
        ['Total', '', '', f"{deducciones:,.0f}"],
    ]
    deducciones_table = Table(deducciones_data, colWidths=[160, 80, 100, 100])
    deducciones_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f4cccc')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#990000')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (1,1), (-1,-2), 'CENTER'),
        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
    ]))
    elementos.append(deducciones_table)
    elementos.append(Spacer(1, 16))

    resumen_data = [
        ['Líquido a recibir', f"{liquido:,.0f}"],
        ['Fecha de generación de nómina', fecha],
    ]
    resumen_table = Table(resumen_data, colWidths=[200, 250])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#c9daf8')),
        ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#0b5394')),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (1,1), (1,1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elementos.append(resumen_table)
    # PDF CONSTRUIDO
    doc.build(elementos)

@app.route('/view-provider', methods=['GET', 'POST'])
def view_provider():
    if request.method == 'POST':
        accion = request.form.get('accion')
        id_proveedor = request.form.get('id')
        nombre = request.form.get('nombre')

        if accion == 'crear':
            insertar_proveedor(nombre)
        elif accion == 'editar':
            actualizar_proveedor(id_proveedor, nombre)
        elif accion == 'eliminar':
            eliminar_proveedor_id(id_proveedor)

        return redirect(url_for('view_provider'))

    # GET
    proveedores = lista_proveedores()
    editar_id = request.args.get('editar_id')
    print("EDITAR_ID:", editar_id)

    proveedor_seleccionado = None

    if editar_id:
        proveedor_seleccionado = obtener_proveedor_por_id(int(editar_id))
        print("Proveedor seleccionado:", proveedor_seleccionado)

    return render_template(
        'Administrator/service_provider.html',
        proveedores=proveedores,
        proveedor_seleccionado=proveedor_seleccionado
    )

@app.route('/proveedores/nuevo')
def nuevo_proveedor():
    return render_template('Administrator/add_provider.html', proveedor_seleccionado=None)

@app.route('/proveedores/eliminar/<int:id>', methods=['POST'])
def eliminar_proveedor(id):
    eliminar_proveedor_id(id)
    return redirect(url_for('view_provider'))

@app.route('/proveedores/guardar', methods=['POST'])
def guardar_proveedor():
    accion = request.form.get('accion')
    nombre = request.form.get('nombre')
    id_proveedor = request.form.get('id')

    if accion == 'crear':
        insertar_proveedor(nombre)
    elif accion == 'editar':
        actualizar_proveedor(id_proveedor, nombre)

    return redirect(url_for('view_provider')) 

#OBTENER CLIENTES ASIGNADOS A ENTRENADOR


@app.route("/guardar_progreso", methods=["POST"])
def guardar_progreso():
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    id_entrenador = session["id_usuario"]
    id_usuario_miembro = request.form["id_usuario_miembro"]
    peso = request.form["peso"]
    descripcion = request.form["descripcion"]

    if existe_avance_hoy(id_usuario_miembro, id_entrenador):
        flash("⚠ Ya registraste un avance para este cliente hoy.", "warning")
        return redirect(url_for("mis_clientes"))

    insertar_progreso(peso, descripcion, datetime.now(), id_usuario_miembro, id_entrenador)

    flash("Avance guardado correctamente.", "success")
    return redirect(url_for("mis_clientes"))

@app.route("/historial-avances")
def historial_avances():
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    id_entrenador = session["id_usuario"]
    avances = obtener_historial_avances(id_entrenador)
    
    return render_template("coach/historial_avances.html", avances=avances)

# @app.route("/perfil-entrenador")
# def perfil_entrenador():
#     if "id_usuario" not in session:
#         return redirect(url_for("login"))

#     id_usuario = session["id_usuario"]

#     entrenador = datos_entrenador(id_usuario)
#     print("Entrenador:", entrenador)

#     if not entrenador:
#         return "No se encontró el perfil del entrenador o no tiene rol 'Entrenador'", 404

#     return render_template('coach/profile.html', entrenador=entrenador) 

# @app.route("/editar-perfil-entrenador", methods=["GET"])
# def editar_perfil_entrenador():
#     if "id_usuario" not in session:
#         return redirect(url_for("login"))
    
#     id_usuario = session["id_usuario"]
#     entrenador = datos_entrenador(id_usuario)
    
#     if not entrenador:
#         flash("No se encontró el entrenador.", "error")
#         return redirect(url_for("perfil_entrenador"))
    
#     return render_template("edit_profile.html", entrenador=entrenador)

# @app.route('/actualizar_perfil_entrenador', methods=['POST'])
# def actualizar_perfil_entrenador():
#     id_usuario =  session["id_usuario"]
#     nombre = request.form['nombre']
#     apellido = request.form['apellido']
#     identificacion = request.form['identificacion']
#     edad = request.form['edad']
#     correo = request.form['correo']
#     telefono = request.form['telefono']
#     contrasena = request.form.get('contrasena', '').strip()

#     if contrasena:
#         contrasena_hash = hash_password(contrasena)
#     else:
#         contrasena_hash = None

#     actualizar_datos_entrenador(id_usuario, nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash)

#     return redirect(url_for('perfil_entrenador'))


#REVISION DE LAS MAQUINAS
@app.route('/maquinas-no-disponibles')
@login_required_admin
def maquinas_no_disponibles():
    maquinas = maquinas_sin_disponibles()
    return jsonify(maquinas)


@app.route("/enviar-revision", methods=["POST"])
def enviar_revision():
    try:
        data = request.get_json()

        id_inventario_maquina = data.get("id_inventario")
        print(f" Inventario recibido: {id_inventario_maquina}")

        id_usuario = session.get("id_usuario")   # admin logueado
        print(f" Usuario (admin) que envía: {id_usuario}")

        observacion_admin = data.get("observacion", "Revisión asignada por el administrador")
        estado = data.get("estado", 1)  # 1 = pendiente

        id_revision = insertar_revision(id_inventario_maquina, id_usuario, observacion_admin, estado)

        return jsonify({"mensaje": f"Máquina enviada a revisión correctamente", "id_revision": id_revision})
    except Exception as e:
        print("Error en enviar_revision:", e)
        return jsonify({"error": str(e)}), 500

#MOSTRAR EL INFORME DE LA REVISION
@app.route("/informes-revision")
def informes_revision():
    reportes = reports_machine()
    return render_template("/Administrator/machine_inspection.html", reportes = reportes)



@app.route('/profile-technical')
def profile_technical():
    revisiones = obtener_revisiones_pendientes()  
    return render_template('Technical/inspections.html', revisiones=revisiones)


@app.route('/tecnico/revisar/<int:id_revision>', methods=['GET', 'POST'])
def revisar_maquina(id_revision):
    if request.method == 'POST':
        estado = request.form['estado']
        observacion_tecnico = request.form['observacion']
        id_usuario = session.get('id_usuario')
        if not id_usuario:
            flash("⚠️ Debes iniciar sesión para registrar una observación.", "warning")
            return redirect(url_for('login'))
        actualizar_estado_revision(id_revision, estado)

        actualizar_observacion_tecnico(id_revision, observacion_tecnico)
        flash("Revisión actualizada correctamente", "success")
        return redirect(url_for('profile_technical'))

    revision = obtener_revision(id_revision)
    observaciones = obtener_observaciones(id_revision)

    return render_template("Technical/review.html", revision=revision, observaciones=observaciones)


# @app.route('/profile')
# def profile_tech():
#     datosTec = lista_tecnicos()
#     print(f"esto llega de {datosTec}")
#     return render_template('Technical/profile.html', datos = datosTec)

# @app.route('/profile/edit/<int:id>', methods=['GET'])
# def edit_profile(id):
#     tecnico = lista_tecnicos(id)
#     return render_template('Technical/edit_profile.html', tecnico=tecnico)

# @app.route('/profile/update/<int:id>', methods=['POST'])
# def update_profile(id):
#     nombre = request.form['nombre']
#     apellido = request.form['apellido']
#     correo = request.form['correo']
#     edad = request.form['edad']
#     contrasena = request.form.get('contrasena')

#     actualizado = actualizar_usuario(id, nombre, apellido, correo, edad)

#     if actualizado:
#         flash("Perfil actualizado correctamente.")
#     else:
#         flash(" No se realizaron cambios.")

#     return redirect(url_for('profile_tech'))

# Mapeo de roles a carpetas
ROL_TO_CARPETA = {
    "miembro": "member",
    "administrador": "administrator",
    "recepcionista": "reception",
    "tecnico": "Technical",
    "entrenador": "coach"
}

@app.route("/profile/<rol>")
def profile(rol):
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    rol_lower = rol.lower()
    if rol_lower not in ROL_TO_CARPETA:
        return f"Rol inválido: {rol}", 400

    usuario = datos_usuario(session["id_usuario"], rol_lower)

    membresia = plan_trabajo = None
    clientes_asignados = []

    if usuario["rol"].lower() == "miembro":
        membresia = obtener_membrehip_user(usuario["identificacion"])
        plan_trabajo = obtener_plan_trabajo(usuario["identificacion"])
    
    if usuario["rol"].lower() == "entrenador":
        clientes_asignados = obtener_clientes_sin_avance_hoy(session["id_usuario"]) or []
        print("CLIENTES:", clientes_asignados)



    return render_template(
    "profile.html",  # único template para todos los roles
    usuario=usuario,
    membresia=membresia,
    plan_trabajo=plan_trabajo,
    clientes_asignados=clientes_asignados,
    carpeta_rol=ROL_TO_CARPETA[rol_lower]
)



@app.route('/profile/edit/<rol>', methods=['GET', 'POST'])
def edit_profile(rol):
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    rol_lower = rol.lower()
    if rol_lower not in ROL_TO_CARPETA:
        return f"Rol inválido: {rol}", 400

    carpeta_rol = ROL_TO_CARPETA[rol_lower]
    usuario = datos_usuario(session["id_usuario"], rol_lower)

    membresia = plan_trabajo = None
    clientes_asignados = []

    if usuario["rol"].lower() == "miembro":
        membresia = obtener_membrehip_user(usuario["identificacion"])
        plan_trabajo = obtener_plan_trabajo(usuario["identificacion"])
    elif usuario["rol"].lower() == "entrenador":
        clientes_asignados = obtener_clientes_sin_avance_hoy(usuario["identificacion"])

    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        identificacion = request.form.get("identificacion")
        edad = request.form.get("edad")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        contrasena = request.form.get("contrasena")

        # Si se ingresó contraseña, aplicar hash antes de enviar
        contrasena_hash = hash_password(contrasena) if contrasena else None

        # Llamar a la función unificada para actualizar datos
        actualizar_datos_usuario(
            id_usuario=usuario["id_usuario"],
            nombre=nombre,
            apellido=apellido,
            identificacion=identificacion,
            edad=edad,
            correo=correo,
            telefono=telefono,
            contrasena_hash=contrasena_hash
        )

        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for("profile", rol=rol_lower))

    return render_template(
        "edit_profile.html",
        usuario=usuario,
        rol=rol_lower,
        carpeta_rol=carpeta_rol,
        membresia=membresia,
        plan_trabajo=plan_trabajo,
        clientes_asignados=clientes_asignados
    )
@app.route('/profile/update/<int:id>', methods=['POST'])
def update_profile(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    telefono = request.form.get('telefono')
    edad = request.form['edad']
    contrasena = request.form.get('contrasena')
    if not contrasena:
        usuario = datos_usuario(id)
        contrasena = usuario['contrasena']
    actualizado = actualizar_usuario(id, nombre, apellido, correo, edad, telefono, contrasena)
    if actualizado:
        flash("Perfil actualizado correctamente.")
    else:
        flash("No se realizaron cambios.")

    return redirect(url_for('profile', rol=session.get('rol','miembro')))

#ASIGNACION DE LAS RUTINAS Y A LOS MIEMBROS
@app.route("/mis-clientes")
def mis_clientes():
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    id_entrenador = session["id_usuario"]
    clientes = obtener_clientes_sin_avance_hoy(id_entrenador)
    return render_template('coach/mis_clientes.html', clientes=clientes)

@app.route("/mis-clientes-rutina")
def mis_clientes_rutina():
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    id_entrenador = session["id_usuario"]
    clientes = obtener_clientes_sin_avance_hoy(id_entrenador)
    return render_template('coach/mis_clientes_rutina.html', clientes=clientes)


@app.route("/ver-plan/<int:id_plan>", methods=['POST'])
def ver_plan(id_plan):
    rutinas = obtener_rutinas_por_plan(id_plan)
    return render_template("coach/ver_plan.html", rutinas=rutinas)

@app.route("/crear-rutina/<int:id_plan>", methods=["GET", "POST"])
def crear_rutina(id_plan):
    if "id_usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        id_maquina = request.form["id_maquina"]
        dia_semana = request.form["dia_semana"]
        zona_nombre = request.form["zona_nombre"]

        # 1. Insertar rutina
        id_rutina = insertar_rutina(nombre, descripcion, id_plan, id_maquina, dia_semana)

        # 2. Insertar zona cuerpo
        insertar_zona_cuerpo(zona_nombre, id_rutina)

        return redirect(url_for("ver_plan", id_plan=id_plan))  # ojo, aquí no necesitas "rutinas.ver_plan"

    # 🔹 Obtener cliente relacionado a ese plan
    cliente = obtener_cliente_por_plan(id_plan)  # debes implementarla en queries
    # 🔹 Obtener lista de máquinas
    # maquinas = obtener_maquinas()  # si ya la tienes hecha

    return render_template(
        "coach/crear_rutina.html",
        id_plan=id_plan,
        cliente=cliente,
        # maquinas=maquinas
    )


if __name__ =='__main__':
    app.run(port =4000, debug =True)