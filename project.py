from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response, send_file
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from query import (validarLogin, check_credentials, login_required_admin, login_required_member,login_required_coach, login_required_receptionist,
                    lista_miembros,lista_genero, plan_trabajo_lista, lista_roles, cant_miembros, cant_entrenadores,
                    conteo_clases_reservadas, add_user, search_users, assig_membreships, list_membreship,
                    guardar_membresia, status_membreship, actualizar_membresia, lista_maquinas, listado_empleados, search_machine, access_users,
                    guardar_acceso, obtener_tipo_acceso, cambiar_estado_acceso, asignar_entrenador, obtener_plan_trabajo, obtener_membrehip_user,
                    save_class_to_db, list_class, delete_class, obtener_reservas_maquinas, obtener_maquinas_disponibles, consultar_reservas_de_hoy, cant_maquinas,
                    cant_proveedores, cant_empleados, obtener_maquinas_disponibles_para_reserva, existe_reserva_en_bloque, registrar_reserva,
                    obtener_id_membresia_usuario, consultar_bloques_contiguos, registrar_pago_nomina, obtener_id_usuario_por_identificacion)

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
    datos = consultar_reservas_de_hoy()  # (id_maquina, nombre_maquina, hora_reservada)

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
            "id_maquina": id_maquina,  # ✅ Ahora sí se envía al frontend
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
    return jsonify(obtener_bloques_disponibles())  # Esto ya lo tienes funcionando


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

    # Asegurar formato completo HH:MM:SS
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

    # Validar si el bloque ya está reservado
    if existe_reserva_en_bloque(id_inventario_maquina, hora_inicio):
        print(">>> BLOQUE YA RESERVADO")
        return jsonify({'success': False, 'message': 'Este bloque ya está reservado'}), 409

    # Validar reserva contigua
    if existe_reserva_contigua(id_membresia_usuario, hora_inicio):
        return jsonify({'success': False, 'message': 'No puedes reservar bloques seguidos'}), 409

    # Registrar reserva
    resultado = registrar_reserva(id_membresia_usuario, id_inventario_maquina, hora_inicio, hora_fin_str)
    return jsonify(resultado), 201 if resultado['success'] else 500


def existe_reserva_contigua(id_membresia_usuario, hora_inicio):
    resultado = consultar_bloques_contiguos(id_membresia_usuario, hora_inicio)
    return resultado is not None

#*************************************************************************

# ENVIAR MAQUINA A REVISION
@app.route('/review-machines', methods=['GET'])
def review_machines():
    asignacion = lista_maquinas()
    return jsonify(asignacion)
#ENVIO DE MAQUINA A REVISION

#LLAMADO AL TEMPLATE MIEMBRO
@app.route('/profile-member')
@login_required_member  # Asegúrate de que este decorador no afecta la sesión
def profile_member():
    identificacion = session.get('identificacion')  # Recupera la identificación
    print(f"Identificación obtenida de la sesión: {identificacion}")
    if not identificacion:
        return redirect(url_for('login'))  # Redirige si no hay identificación
    
    plan_trabajo = obtener_plan_trabajo(identificacion)
    membresia_asignada = obtener_membrehip_user(identificacion)
    return render_template('member/profile.html', plan_trabajo=plan_trabajo, membresia = membresia_asignada)

#TEMPLETE PRINCIPAL DEL MIEMBRO
@app.route('/inicio')
def index_member():
    identificacion = session.get('identificacion')
    return render_template('member/index.html')

#RESERVAR MÁQUINAS ***********************************************************
# 1. Controlador que retorna las máquinas disponibles en JSON
@app.route('/api/maquinas_disponibles', methods=['GET'])
def api_maquinas_disponibles():
    maquinas = obtener_maquinas_disponibles_para_reserva()
    resultado = [{"id": m[0], "nombre": m[1]} for m in maquinas]
    return jsonify(resultado)


# *************************************************************************





# @app.route('/machine-reservation', methods=['POST'])

# def machine_reservation():
#     if request.content_type != 'application/json':
#         return jsonify({"message": "El Content-Type debe ser application/json", "success": False}), 415

#     # Depuración para revisar los datos de la solicitud
#     try:
#         print("Encabezados:", request.headers)  # Ver los encabezados enviados en la solicitud
#         print("Datos crudos:", request.data)  # Ver los datos crudos del body
#         print("JSON procesado:", request.get_json())  # Intentar obtener el JSON de forma explícita

#         # Si llega el JSON correctamente, trata los valores
#         data = request.get_json()
#         print("Datos JSON procesados:", data)
#     except Exception as e:
#         print("Error al procesar JSON:", e)  # Imprimir error si la conversión falla
#         return jsonify({"message": "Error al procesar el JSON", "success": False}), 400

#     # Valida los campos que se requieren
#     machine = data.get('machine')
#     date = data.get('date')
#     start_time = data.get('start_time')

#     if not all([machine, date, start_time]):
#         return jsonify({"message": "Faltan datos en la solicitud.", "success": False}), 400

#     # Procesar la reserva
#     end_time = (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=15)).strftime("%H:%M")
#     # Procesar base de datos, hacer queries, etc.

#     return jsonify({
#         "message": "Reserva realizada correctamente",
#         "success": True
#     }), 201

#LLAMADO AL TEMPLATE ENTRENADOR
@app.route('/profile-coach')
@login_required_coach
def profile_coach():
    return render_template('coach/profile.html')

@app.route('/profile-receptionist', methods=['GET', 'POST'])
@login_required_receptionist
def profile_receptionist():
    return render_template('receptionist/profile.html')  # Asegúrate de que resultados tenga un valor



    

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
        id_usuario = int(id_usuario_str) 
    except ValueError:
        return jsonify({'error': 'ID de usuario debe ser un número válido'}), 400

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

#MOSTRAR PLAN DE TRABAJO DEL MIEMBRO

#MOSTRAR OPCIONES PARA CLASES
@app.route('/acciones-clase')
def acciones_clase():
    return render_template('Administrator/options_class.html')

#CREACION DE LAS CLASES
@app.route('/create-class', methods=['GET'])
def show_create_class_form():
    return render_template('Administrator/create_class.html')

# Ruta para procesar la creación de la clase
@app.route('/create-class', methods=['POST'])
def create_class():
    # Obtén los datos del formulario directamente
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

# @app.route('/delete-class', methods=['GET', 'POST'])
# def delete_class_admin():
#     classes = list_class()
#     return render_template('Administrator/delete_class.html', clases=classes)

@app.route('/formulario-nomina')
def mostrar_formulario_nomina():
    try:
        empleados =  listado_empleados()
        return render_template('Administrator/nomina.html', empleados=empleados)
    except Exception as e:
        print(f"Error al cargar formulario de nómina: {e}")
        flash("Error cargando formulario", "error")
        return redirect(url_for('home'))  # Ajusta según tu ruta principal


from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

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
        fecha_generacion = request.form.get('fecha_pago', '')

        salario_base = float(request.form.get('salario', 0) or 0)
        auxilio_transporte = float(request.form.get('auxilio', 0) or 0)
        aporte_salud = float(request.form.get('salud', 0) or 0)
        aporte_pension = float(request.form.get('pension', 0) or 0)
        total_devengado = float(request.form.get('total_devengado', 0) or 0)
        total_deducciones = float(request.form.get('total_deducciones', 0) or 0)
        liquido_a_recibir = float(request.form.get('liquido', 0) or 0)

        # Registro en la base de datos (SIN CAMBIOS)
        datos = (
            id_usuario, fecha_generacion, salario_base,
            auxilio_transporte, aporte_salud, aporte_pension,
            total_devengado, total_deducciones, liquido_a_recibir
        )

        exito = registrar_pago_nomina(datos)

        if exito:
            # Ruta donde se guardará el PDF (dentro del proyecto)
            carpeta_pdfs = os.path.join(os.getcwd(), "static", "pdfs")
            os.makedirs(carpeta_pdfs, exist_ok=True)
            ruta_pdf = os.path.join(carpeta_pdfs, f"nomina_{identificacion}.pdf")

            # Generar el PDF
            c = canvas.Canvas(ruta_pdf, pagesize=letter)
            c.drawString(100, 750, f"Nómina - ID Usuario: {id_usuario}")
            c.drawString(100, 730, f"Fecha de Pago: {fecha_generacion}")
            c.drawString(100, 710, f"Salario Base: {salario_base}")
            c.drawString(100, 690, f"Auxilio Transporte: {auxilio_transporte}")
            c.drawString(100, 670, f"Aporte Salud: {aporte_salud}")
            c.drawString(100, 650, f"Aporte Pensión: {aporte_pension}")
            c.drawString(100, 630, f"Total Devengado: {total_devengado}")
            c.drawString(100, 610, f"Total Deducciones: {total_deducciones}")
            c.drawString(100, 590, f"Líquido a Recibir: {liquido_a_recibir}")
            c.save()

            return send_file(ruta_pdf, as_attachment=True)

        else:
            return "Error al registrar en la base de datos", 500

    except Exception as e:
        print("Error en /insertar-nomina:", e)
        return "Error al procesar la solicitud", 500


# 📌 Función para generar PDF
def generar_pdf(ruta, identificacion, fecha, salario, auxilio, salud, pension, devengado, deducciones, liquido):
    doc = SimpleDocTemplate(ruta, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Comprobante de Nómina", estilos["Title"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"Empleado ID: {identificacion}", estilos["Normal"]))
    elementos.append(Paragraph(f"Fecha de pago: {fecha}", estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    data = [
        ["Concepto", "Valor"],
        ["Salario Base", f"${salario:,.2f}"],
        ["Auxilio Transporte", f"${auxilio:,.2f}"],
        ["Aporte Salud", f"${salud:,.2f}"],
        ["Aporte Pensión", f"${pension:,.2f}"],
        ["Total Devengado", f"${devengado:,.2f}"],
        ["Total Deducciones", f"${deducciones:,.2f}"],
        ["Líquido a Recibir", f"${liquido:,.2f}"],
    ]

    tabla = Table(data, colWidths=[200, 150])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))

    elementos.append(tabla)
    doc.build(elementos)

if __name__ =='__main__':
    app.run(port =4000, debug =True)