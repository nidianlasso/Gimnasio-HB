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
        rol = info_user[0]  # Obtener el rol del usuario
        resp = make_response()  # Crear la respuesta base

        # Redirigir según el rol del usuario
        if rol == "Administrador":
            resp = make_response(redirect(url_for('administrator')))
        elif rol == "Miembro":
            resp = make_response(redirect(url_for('profile_member')))
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
    cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE identificacion = %s AND contrasena = %s", (identificacion, contrasena))
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

def access_users(identificacion):
    cursor.execute("""
        SELECT u.id_usuario, u.nombre, u.apellido, r.nombre AS rol
        FROM usuario u
        INNER JOIN rol r ON u.id_rol = r.id_rol
        WHERE u.identificacion = %s
    """, (identificacion,))
    resultado = cursor.fetchall()
    return resultado


# def guardar_acceso(fecha, duracion, tipo_acceso, id_usuario): 
#     try:
#         # Verificar si el usuario existe
#         cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
#         resultado_usuario = cursor.fetchone()

#         if resultado_usuario is None:
#             print(f"Usuario con ID {id_usuario} no encontrado.")
#             return False  # O puedes optar por crear el usuario aquí si lo deseas

#         # Formatear la fecha
#         fecha_dt = datetime.strptime(fecha[:-1], '%Y-%m-%dT%H:%M:%S.%f')
#         fecha_str = fecha_dt.strftime('%Y-%m-%d %H:%M:%S')
        
#         # Asegúrate de definir duracion_str aquí
#         duracion_str = str(duracion)  # Cambia esto si tienes otra lógica para duración
        
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 'INSERT INTO acceso (fecha, duracion, tipo_acceso, id_usuario) VALUES (%s, %s, %s, %s)',
#                 (fecha_str, duracion_str, tipo_acceso, id_usuario)
#             )
#             connection.commit()
        
#         return True
#     except Exception as e:
#         print("Error al guardar el acceso:", e)
#         print("Datos a registrar en el acceso:", fecha, duracion_str, tipo_acceso, id_usuario)
#         return False

# def guardar_acceso(fecha, duracion, tipo_acceso, id_usuario):
#     try:
#         # Verificar si el usuario existe
#         cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
#         resultado_usuario = cursor.fetchone()

#         if resultado_usuario is None:
#             print(f"Usuario con ID {id_usuario} no encontrado.")
#             return False  # O puedes optar por crear el usuario aquí si lo deseas

#         # Aquí puedes registrar el acceso
#         cursor.execute(
#             "INSERT INTO acceso (fecha, duracion, tipo_acceso, id_usuario) VALUES (%s, %s, %s, %s)",
#             (fecha, duracion, tipo_acceso, id_usuario)
#         )
#         connection.commit()  # Asegúrate de que esto esté habilitado en tu conexión

#         print("Acceso registrado:", fecha, duracion, tipo_acceso, id_usuario)
#         return True
#     except Exception as e:
#         print("Error al guardar el acceso:", e)
#         print("Datos a registrar en el acceso:", fecha, duracion, tipo_acceso, id_usuario)
#         return False

def guardar_acceso(fecha, duracion, tipo_acceso, id_usuario):
    try:
        print("Intentando guardar acceso...")
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        resultado_usuario = cursor.fetchone()

        if resultado_usuario is None:
            print(f"Usuario con ID {id_usuario} no encontrado.")
            return False
        
        # Formatear la fecha
        fecha_dt = datetime.strptime(fecha[:-1], '%Y-%m-%dT%H:%M:%S.%f')
        fecha_str = fecha_dt.strftime('%Y-%m-%d %H:%M:%S')
                
        # Asegúrate de definir duracion_str aquí
        duracion_str = str(duracion)  # Cambia esto si tienes otra lógica para duración
        

        print("Usuario encontrado, guardando acceso...")
        cursor.execute('INSERT INTO acceso (fecha, duracion, tipo_acceso, id_usuario) VALUES (%s, %s, %s, %s)',
                (fecha_str, duracion_str, tipo_acceso, id_usuario))
        connection.commit()
        print("Acceso guardado exitosamente.")
        return True
    except Exception as e:
        print("Error al guardar el acceso:", e)
        return False

def obtener_tipo_acceso(id_usuario):
    try:
        # Verificar si el usuario existe en la base de datos
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        resultado_usuario = cursor.fetchone()
        
        if resultado_usuario is None:
            print(f'El usuario ID: {id_usuario} no existe en la tabla usuarios')
            return None
        
        # Verificar el tipo de acceso del usuario
        cursor.execute("SELECT a.tipo_acceso FROM acceso a WHERE a.id_usuario = %s", (id_usuario,))
        resultado_acceso = cursor.fetchone()
        
        if resultado_acceso is None:
            print(f'No se encontró acceso para el usuario ID: {id_usuario}. Creando acceso por defecto.')
            # Crear un acceso por defecto
            fecha = datetime.now().isoformat()  # Fecha actual
            duracion = 60  # Duración predeterminada
            tipo_acceso = 'Inactive'  # Tipo de acceso inicial

            # Intentar guardar el nuevo acceso
            if not guardar_acceso(fecha, duracion, tipo_acceso, id_usuario):
                print("Error al crear el acceso.")
                return None
            
            # Después de crear el acceso, devolvemos el tipo de acceso
            return tipo_acceso
        
        # Si el acceso existe, imprimimos el tipo actual
        print(resultado_acceso, "ESTE ES EL TIPO DE ACCESO QUE TIENE")
        return resultado_acceso[0]
    
    except Exception as e:
        raise Exception(f'Error en la consulta: {str(e)}')

def cambiar_estado_acceso(id_usuario):
    try:
        # Obtener el acceso activo actual
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
            "UPDATE acceso SET tipo_acceso = 'Inactive', duracion_seconds = %s WHERE id_usuario = %s AND tipo_acceso = 'Active'",
            (duracion_seconds, id_usuario)
        )
        connection.commit()

        return {'message': 'Estado de acceso cambiado a Inactive exitosamente.', 'duracion': duracion_seconds}

    except Exception as e:
        return {'error': f'Error al cambiar el estado del acceso: {str(e)}'}

