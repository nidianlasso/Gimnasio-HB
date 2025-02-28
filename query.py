from flask_mysqldb import MySQL
import pymysql
from functools import wraps
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
from datetime import datetime

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
        rol, user_identificacion = info_user
        session['identificacion'] = user_identificacion
        resp = make_response()  # Crear la respuesta base

        # Redirigir según el rol del usuario
        if rol == "Administrador":
            resp = make_response(redirect(url_for('administrator')))
        elif rol == "Miembro":
            plan_trabajo = obtener_plan_trabajo(user_identificacion)
            resp = make_response(redirect(url_for('index_member')))
            resp.set_cookie('plan_trabajo', plan_trabajo)
        elif rol == "Entrenador":
            resp = make_response(redirect(url_for('profile_coach')))
        elif rol == "Recepcionista":
            resp = make_response(redirect(url_for('profile_receptionist')))
        # Devolver la respuesta con la cookie establecida
        resp.set_cookie('identificacion', identificacion)  
        return resp  

    # Si las credenciales son incorrectas, mostrar error
    error = "Credenciales incorrectas. Intente de nuevo."
    return render_template('login.html', error=error)

# Función para verificar las credenciales en la base de datos
def check_credentials(identificacion, contrasena):
    cursor.execute("SELECT r.nombre, u.identificacion FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE identificacion = %s AND contrasena = %s", (identificacion, contrasena))
    info_user = cursor.fetchone()
    print("Resultado de la consulta para el login del usuario:")
    print(info_user)  # Verificación del resultado de la consulta para depurar
    return info_user

#--GUARDAR LA COKKIE
def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si la cookie 'identificacion' está presente
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre ='Administrador'", (identificacion))
            rol_user = cursor.fetchall()
            if len(rol_user) == 0:  # Si no hay cookie, redirigir al login
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        # Si la cookie existe, proceder a la función protegida
        return f(*args, **kwargs)
    return decorated_function


def login_required_member(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si la cookie 'identificacion' está presente
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre ='Miembro'", (identificacion))
            rol_user = cursor.fetchall()
            print(rol_user, "ROOOOOL DEL USUARIO")
            if len(rol_user) == 0:  # Si no hay cookie, redirigir al login
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        # Si la cookie existe, proceder a la función protegida
        return f(*args, **kwargs)
    return decorated_function

def login_required_coach(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si la cookie 'identificacion' está presente
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            print(f"Identificación de la cookie: {identificacion}")  # Debug: Verifica el valor de la cookie
            # Realizar la consulta para verificar el rol del usuario
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre = 'Entrenador'", (identificacion))
            rol_user = cursor.fetchall()
            print(f"Rol del usuario: {rol_user}")  # Debug: Verifica los resultados de la consulta
            if len(rol_user) == 0:  # Si no hay rol "Entrenador", redirigir al login
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            print("Cookie de identificación no encontrada. Redirigiendo al login.")
            return redirect(url_for('login'))
        
        # Si la cookie existe y el rol es correcto, proceder a la función protegida
        return f(*args, **kwargs)
    return decorated_function

def login_required_receptionist(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si la cookie 'identificacion' está presente
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            print(f"Identificación de la cookie: {identificacion}")  # Debug: Verifica el valor de la cookie
            # Realizar la consulta para verificar el rol del usuario
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre = 'Recepcionista'", (identificacion))
            rol_user = cursor.fetchall()
            print(f"Rol del usuario: {rol_user}")  # Debug: Verifica los resultados de la consulta
            if len(rol_user) == 0:  # Si no hay rol "Entrenador", redirigir al login
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            print("Cookie de identificación no encontrada. Redirigiendo al login.")
            return redirect(url_for('login'))
        
        # Si la cookie existe y el rol es correcto, proceder a la función protegida
        return f(*args, **kwargs)
    return decorated_function

#--GUARDAR LA COKKIE


#OBTENER EL LISTADO DE MIEMBROS PARA GESTION
def lista_miembros():
    cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, u.edad, u.correo, u.telefono, r.nombre FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol")
    listado_miembros = cursor.fetchall()
    return listado_miembros
#OBTENER EL LISTADO DE MIEMBROS

#--LISTADO DE GENERO
def lista_genero():
    cursor.execute("SELECT id_genero, tipo FROM genero")
    result_gender= cursor.fetchall()
    return result_gender
#--LISTADO DE GENERO

#--LISTADO PLAN TRABAJO
def plan_trabajo_lista():
    cursor.execute("SELECT id_plan_trabajo, nombre FROM plan_trabajo")
    result_plan_trabajo= cursor.fetchall()
    return result_plan_trabajo
#--LISTADO PLAN TRABAJO

#--LISTADO roles
def lista_roles():
    cursor.execute("SELECT id_rol, nombre FROM rol")
    result_rol= cursor.fetchall()
    return result_rol
#--LISTADO roles

#OBTENER LA CANTIDAD DE ROLES
def cant_miembros():
    cursor.execute("SELECT COUNT(*) AS listado_miembros FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE r.nombre = 'Miembro';")
    resul_lista = cursor.fetchone()[0]
    return resul_lista

def cant_entrenadores():
    cursor.execute("SELECT COUNT(*) AS listado_entrenadores FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE r.nombre = 'Entrenador'")
    resul_lista_entrenador = cursor.fetchone()[0]
    return resul_lista_entrenador

def conteo_clases_reservadas():
    cursor.execute("SELECT COUNT(*) AS listado_entrenadores FROM reserva_clase")
    result_lista_reservas = cursor.fetchone()[0]
    return result_lista_reservas

#OBTENER LA CANTIDAD DE ROLES

#--AGREGAR USUARIO
def add_user(identificacion, nombre, apellido, edad, correo, telefono, genero, plan_trab, rol, contrasena):
    try:
        cursor.execute('INSERT INTO usuario (identificacion, nombre, apellido, edad, correo, telefono, id_genero, id_plan_trabajo, id_rol, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                (identificacion, nombre, apellido, edad, correo, telefono, genero, plan_trab, rol, contrasena))
        #Guardar la info en la base de datos
        connection.commit()
        return True
    except Exception as e:
        #---Guardar la info en la base de datos
        print("Informacion que se sube a la base")
        print(identificacion, nombre, apellido, edad, correo, telefono, genero, plan_trab, rol, contrasena)
        return False # Retorna False si no se ha procesado el formulario
#--AGREGAR USUARIO

#BUSQUEDA DE USUARIOS
def search_users(identificacion):
    cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, u.edad, u.correo, u.telefono, g.tipo AS genero, p.nombre AS plan_trabajo, r.nombre AS rol FROM usuario u INNER JOIN genero g ON u.id_genero = g.id_genero INNER JOIN plan_trabajo p ON u.id_plan_trabajo = p.id_plan_trabajo INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s", (identificacion))
    result_busqueda = cursor.fetchall()
    return result_busqueda

#ASIGNACION DE MEMBRESIAS
def assig_membreships():
    try:
        cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, m.costo, m.tipo, mu.fecha_inicio, mu.fecha_fin, em.nombre AS estado_membresia, u.id_usuario, mu.id_membresia_usuario, m.id_membresia FROM usuario u LEFT JOIN membresia_usuario mu ON mu.id_usuario = u.id_usuario LEFT JOIN membresia m ON mu.id_membresia = m.id_membresia LEFT JOIN estado_membresia em ON mu.id_estado_membresia = em.id_estado_membresia WHERE u.id_rol= '5';")
        campos_asignacion = cursor.fetchall()
        return campos_asignacion
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

#LISTA DE MEMBRESIAS
def list_membreship():
    cursor.execute('SELECT tipo, costo, id_membresia FROM membresia')
    resul_lista_membresia = cursor.fetchall()
    print(resul_lista_membresia, "estos son los tipos de membresias")
    return resul_lista_membresia

#LISTA DE MIEMBROS
def list_user_member():
    cursor.execute('SELECT identificacion, nombre, apellido, correo, id_usuario FROM usuario WHERE id_rol =5')
    listado_miembros = cursor.fetchone()[0]
    return listado_miembros

def guardar_membresia(usuario_id, tipo, fecha_inicio, fecha_fin, estado):
    try:
        cursor.execute(
            'INSERT INTO membresia_usuario(id_usuario, id_membresia, fecha_inicio, fecha_fin, id_estado_membresia) VALUES (%s, %s, %s, %s, %s)', 
            (usuario_id, tipo, fecha_inicio, fecha_fin, estado)
        )
        connection.commit()
        return True
    except Exception as e:
        print("Error al guardar la membresía:", e)
        print("Información que se sube a la base de datos:", usuario_id, tipo, fecha_inicio, fecha_fin, estado)
        return False  # Retorna False si no se ha procesado el formulario

#ESTADO DE LA MEMBRESIA
def status_membreship():
    cursor.execute("SELECT id_estado_membresia, nombre FROM estado_membresia")
    status = cursor.fetchall()
    return status

#ACTUALIZAR MEMBRESIA
def actualizar_membresia( tipo, fecha_inicio, fecha_fin, estado, id_membresia_usuario):
    try:
        cursor.execute('UPDATE membresia_usuario SET id_membresia=%s, fecha_inicio=%s, fecha_fin=%s, id_estado_membresia=%s WHERE id_membresia_usuario=%s',
               (tipo, fecha_inicio, fecha_fin, estado, id_membresia_usuario))

        connection.commit()
        return True
    except Exception as e:
        print("Error al actualizar la membresía:", e)
        print("Información que se intenta actualizar:", tipo, fecha_inicio, fecha_fin, estado, id_membresia_usuario)
        return False


#OBTENER EL LISTADO DE MIEMBROS PARA GESTION
def lista_maquinas():
    cursor.execute("SELECT m.nombre, i.serial, i.fecha_compra, i.precio, p.nombre, i.disponibilidad FROM inventario_maquina i INNER JOIN maquina m ON i.id_maquina = m.id_maquina INNER JOIN proveedor p ON i.id_proveedor = p.id_proveedor")
    listado_maquinas = cursor.fetchall()
    return listado_maquinas
#OBTENER EL LISTADO DE MIEMBROS

#BUSQUEDA DE MAQUINAS
def search_machine(nombre):
    cursor.execute("SELECT m.nombre, i.fecha_compra, i.serial, p.nombre, i.precio FROM inventario_maquina i INNER JOIN maquina m ON i.id_maquina = m.id_maquina INNER JOIN proveedor p ON i.id_proveedor = p.id_proveedor  WHERE m.nombre = %s", (nombre,))
    result_busqueda = cursor.fetchall()
    return result_busqueda

#OBTENER LA INFORMACION DE LAS MAQUINAS EN LOS HORARIOS DISPONIBLES Y AGENDADOS
def info_machine():
    cursor.execute('''SELECT rm.fecha, rm.hora_inicio, rm.hora_fin, u.nombre, u.apellido, m.nombre FROM reserva_maquina rm INNER JOIN membresia_usuario mu ON rm.id_membresia_usuario = mu.id_membresia_usuario INNER JOIN usuario u ON mu.id_usuario = u.id_usuario INNER JOIN inventario_maquina im ON im.id_inventario_maquina = rm.id_inventario_maquina INNER JOIN maquina m ON m.id_maquina = im.id_maquina ORDER BY rm.fecha, rm.hora_inicio;''')
    result_busqueda = cursor.fetchall()
    print("Usuario con maquina reservada:", result_busqueda)  # Depuración
    return result_busqueda


#CREAR EL ACCESO DE LOS USUARIOS QUE INGRESAN O SALEN DEL GIMNASIO
def access_users(identificacion):
    cursor.execute("""
        SELECT u.id_usuario, u.nombre, u.apellido, r.nombre AS rol
        FROM usuario u
        INNER JOIN rol r ON u.id_rol = r.id_rol
        WHERE u.identificacion = %s
    """, (identificacion,))
    resultado = cursor.fetchall()
    return resultado

def guardar_acceso(fecha, duracion, tipo_acceso, id_usuario):
    try:
        print("Intentando guardar acceso...")
        cursor.execute("SELECT * FROM acceso WHERE id_usuario = %s AND tipo_acceso = 'Active'", (id_usuario,))
        resultado_acceso = cursor.fetchone()

        # Asegúrate de convertir la fecha a un formato correcto
        fecha_dt = datetime.strptime(fecha[:-1], '%Y-%m-%dT%H:%M:%S.%f')  # Elimina la 'Z'
        fecha_str = fecha_dt.strftime('%Y-%m-%d %H:%M:%S')

        if resultado_acceso is None:
            # Si no hay acceso activo, insertar un nuevo acceso
            print("No hay acceso activo, creando uno nuevo...")
            cursor.execute('INSERT INTO acceso (fecha, duracion, tipo_acceso, id_usuario) VALUES (%s, %s, %s, %s)',
                           (fecha_str, duracion, tipo_acceso, id_usuario))
        else:
            # Si hay acceso activo, actualizarlo
            print("Actualizando acceso existente...")
            cursor.execute('UPDATE acceso SET fecha = %s, duracion = %s, tipo_acceso = %s WHERE id_usuario = %s AND tipo_acceso = %s',
                           (fecha_str, duracion, tipo_acceso, id_usuario, 'Active'))

        connection.commit()
        print("Acceso guardado/actualizado exitosamente.")
        return True
    except Exception as e:
        print("Error al guardar el acceso:", e)
        return False

def obtener_tipo_acceso(id_usuario):
    try:
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        resultado_usuario = cursor.fetchone()
        
        if resultado_usuario is None:
            print(f'El usuario ID: {id_usuario} no existe en la tabla usuarios')
            return None
        
        cursor.execute("SELECT a.tipo_acceso FROM acceso a WHERE a.id_usuario = %s", (id_usuario,))
        resultado_acceso = cursor.fetchone()
        
        if resultado_acceso is None:
            print(f'No se encontró acceso para el usuario ID: {id_usuario}. Creando acceso por defecto.')
            fecha = datetime.now().isoformat()
            duracion = 60
            tipo_acceso = 'Inactive'
            
            if not guardar_acceso(fecha, duracion, tipo_acceso, id_usuario):
                print("Error al crear el acceso.")
                return None
            
            return {'tipo_acceso': tipo_acceso}  # Devolver un objeto

        return {'tipo_acceso': resultado_acceso[0]}  # Asegúrate de devolver un objeto
    except Exception as e:
        raise Exception(f'Error en la consulta: {str(e)}')

def cambiar_estado_acceso(id_usuario):
    try:
        cursor.execute("SELECT * FROM acceso WHERE id_usuario = %s AND tipo_acceso = 'Active'", (id_usuario,))
        acceso_actual = cursor.fetchone()

        if acceso_actual is None:
            return {'error': f"No se encontró acceso activo para el usuario ID: {id_usuario}."}

        # Calcular la duración
        fecha_inicio = acceso_actual['fecha']
        fecha_fin = datetime.now()
        duracion_seconds = int((fecha_fin - fecha_inicio).total_seconds())

        # Actualizar el acceso a Inactive
        cursor.execute(
            "UPDATE acceso SET tipo_acceso = 'Inactive', duracion = %s WHERE id_usuario = %s AND tipo_acceso = 'Active'",
            (duracion_seconds, id_usuario)
        )
        connection.commit()

        return {'message': 'Estado de acceso cambiado a Inactive exitosamente.', 'duracion': duracion_seconds}

    except Exception as e:
        return {'error': f'Error al cambiar el estado del acceso: {str(e)}'}

#ASIGNAR ENTRENADOR
def asignar_entrenador():
    cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, a.id_acceso, a.tipo_acceso, a.fecha, r.nombre AS nombre_rol, u.id_usuario, pt.nombre FROM acceso a INNER JOIN usuario u ON a.id_usuario = u.id_usuario INNER JOIN rol r ON u.id_rol = r.id_rol INNER JOIN plan_trabajo pt ON pt.id_plan_trabajo = u.id_plan_trabajo  WHERE r.nombre IN ('Miembro', 'Entrenador') AND a.tipo_acceso = 'Active' AND DATE(a.fecha) = CURDATE();")
    resultado = cursor.fetchall()
    print('ESTE ES EL RESULTADO DE LA CONSULTA')
    print(resultado)
    return resultado

#MIEMBRO
#OBTENER PLAN DE TRABAJO DEL MIEMBRO
def obtener_plan_trabajo(identificacion):
    cursor.execute(
        "SELECT p.nombre FROM usuario u INNER JOIN plan_trabajo p ON u.id_plan_trabajo = p.id_plan_trabajo WHERE u.identificacion = %s", 
        (identificacion,))
    plan = cursor.fetchone()
    return plan[0] if plan else None  # Retorna el plan o None si no exise

def obtener_membrehip_user(identificacion):
    cursor.execute("SELECT m.tipo, e.nombre FROM membresia_usuario mu INNER JOIN membresia m ON mu.id_membresia = m.id_membresia INNER JOIN estado_membresia e ON mu.id_estado_membresia = e.id_estado_membresia INNER JOIN usuario u ON mu.id_usuario = u.id_usuario WHERE u.identificacion = %s",
                   (identificacion,))
    membresia_usuario = cursor.fetchone()
    return membresia_usuario

def assig_machine():
    try:
        cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, m.costo, m.tipo, mu.fecha_inicio, mu.fecha_fin, em.nombre AS estado_membresia, u.id_usuario, mu.id_membresia_usuario, m.id_membresia FROM usuario u LEFT JOIN membresia_usuario mu ON mu.id_usuario = u.id_usuario LEFT JOIN membresia m ON mu.id_membresia = m.id_membresia LEFT JOIN estado_membresia em ON mu.id_estado_membresia = em.id_estado_membresia WHERE u.id_rol= '5';")
        campos_asignacion = cursor.fetchall()
        return campos_asignacion
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

def status_membreship_member(identificacion):
    cursor.execute("SELECT u.nombre, u.apellido, em.nombre FROM membresia_usuario mu INNER JOIN usuario u ON mu.id_usuario = u.id_usuario INNER JOIN estado_membresia em ON mu.id_estado_membresia = em.id_estado_membresia WHERE u.identificacion = %s", 
        (identificacion,))
    estado_membresia = cursor.fetchone()
    return estado_membresia

# def count_reservation_machine(id_maquina, hora_inicio, hora_fin, fecha):
#     cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_inventario_maquina = %s AND fecha = %s AND ( (hora_inicio >= %s AND hora_fin <=%s) );", 
#         (id_maquina, fecha, hora_inicio, hora_fin, hora_inicio, hora_fin))
#     count = cursor.fetchone()[0]
#     return count

# #CREAR RESERVA DE LA MAQUINA
# def insert_reservation(id_membresia_usuario, id_maquina, fecha, hora_inicio, hora_fin):
#     try: cursor.execute("INSERT INTO reserva (fecha, hora_inicio, hora_fin, id_membresia_usuario, id_inventario_maquina) VALUES (%s, %s, %s, %s, %s)",
#         (fecha, hora_inicio, hora_fin, id_membresia_usuario, id_maquina))
#     except Exception as e:
#         print(f"ERROR AL CREAR LA RESERVA {e}")
#         return []

# # Lógica para procesar la reserva
# def process_reservation(id_membresia_usuario, id_maquina, fecha, hora_inicio, hora_fin):
#     # Contar conflictos de horarios
#     conflictos = count_reservation_machine(id_maquina, hora_inicio, hora_fin, fecha)
#     if conflictos > 0:
#         return {"success": False, "message": "La máquina no está disponible en el rango seleccionado."}

#     # Insertar la reserva si no hay conflictos
#     insert_reservation(id_membresia_usuario, id_maquina, fecha, hora_inicio, hora_fin)
#     return {"success": True, "message": "Reserva registrada exitosamente."}

# def handle_sql_queries(machine_id, date, start_time, end_time, membership_id):
#     # Comprobar si hay conflicto de reservas
#     cursor.execute = ("""SELECT * FROM reserva
#     WHERE id_inventario_maquina = %s AND fecha = %s 
#     AND ((%s BETWEEN hora_inicio AND hora_fin) OR (%s BETWEEN hora_inicio AND hora_fin));
#     """,(machine_id, date, start_time, end_time))
#     conflict = cursor.fetchone()

#     if conflict:
#         return {"success": False, "message": "La máquina ya está reservada en este horario."}

#     # Insertar nueva reserva
#     cursor.execute = ( """
#     INSERT INTO reserva (fecha, hora_inicio, hora_fin, id_membresia_usuario, id_inventario_maquina)
#     VALUES (%s, %s, %s, %s, %s);
#     """
#     (date, start_time, end_time, membership_id, machine_id))
#     connection.commit()
#     return {"success": True, "message": "Reserva realizada con éxito."}



# Función para guardar la clase en la base de datos ADMINISTRADOR
def save_class_to_db(nombre, fecha_inicio, hora, duration):
    try:
        cursor.execute('INSERT INTO clase (nombre, fecha_inicio, hora, duracion) VALUES (%s, %s, %s, %s)', (nombre, fecha_inicio, hora, duration))
        connection.commit()
        return {'success': True, 'message': 'Clase guardada exitosamente'}
    except pymysql.MySQLError as e:
        return {'success': False, 'message': f'Error al guardar en la base de datos: {e}'}

#Reserva de clase usuario
def reservation_class():
    return True

#Obtener maquinas
def get_maquinas():
    cursor.execute("SELECT id_maquina, nombre FROM maquina")
    maquinas = [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
    return jsonify(maquinas)