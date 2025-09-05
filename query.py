from flask_mysqldb import MySQL
import pymysql
from functools import wraps
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_folder='static', template_folder='template')
connection = pymysql.connect(host="localhost", user="root", passwd="12345", database="bd_gimnasio2")
cursor = connection.cursor()

def hash_password(password):
    # Genera un hash
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    # Verifica si la contraseña coincide con el hash
    return check_password_hash(hashed_password, password)

def obtenerUsuarios():
    cursor.execute("SELECT * FROM bd_gimnasio2.usuario")
    rows = cursor.fetchall()
    cursor.close()  
    return rows


# Función para validar el login del usuario
def validarLogin(identificacion, contrasena):
    info_user = check_credentials(identificacion, contrasena)
    
    if info_user:
        rol = info_user['rol']
        user_identificacion = info_user['identificacion']
        id_usuario = info_user['id_usuario']

        session['id_usuario'] = id_usuario
        session['identificacion'] = user_identificacion
        session['rol'] = rol.lower()

        resp = make_response()

        if rol.lower() == "administrador":
            resp = redirect(url_for('administrator'))
        elif rol.lower() == "miembro":
            plan_trabajo = obtener_plan_trabajo(user_identificacion)
            resp = redirect(url_for('index_member'))
            resp.set_cookie('plan_trabajo', plan_trabajo)
        elif rol.lower() == "entrenador":
            resp = redirect(url_for('index_coach'))
        elif rol.lower() == "recepcionista":
            resp = redirect(url_for('index_receptionist'))
        elif rol.lower() == "tecnico":
            resp = redirect(url_for('profile_technical'))

        resp.set_cookie('identificacion', str(user_identificacion))
        return resp

    error = "Credenciales incorrectas. Intente de nuevo."
    return render_template('login.html', error=error)



# Función para verificar las credenciales en la base de datos
def check_credentials(identificacion, contrasena):
    cursor.execute("""
        SELECT LOWER(r.nombre) AS rol, u.identificacion, u.id_usuario, u.contrasena
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        WHERE u.identificacion = %s
    """, (identificacion,))

    row = cursor.fetchone()
    if row:
        rol, identificacion_db, id_usuario, stored_password = row

        # Intenta verificar si la contraseña está hasheada
        try:
            if check_password_hash(stored_password, contrasena):
                return {'rol': rol, 'identificacion': identificacion_db, 'id_usuario': id_usuario}
        except ValueError:
            # Si no es un hash válido (por ejemplo, texto plano), ignora error
            pass

        # Si no es hash válido, intenta comparación directa
        if contrasena == stored_password:
            return {'rol': rol, 'identificacion': identificacion_db, 'id_usuario': id_usuario}

    return None




#--GUARDAR LA COKKIE
def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre ='Administrador'", (identificacion))
            rol_user = cursor.fetchall()
            if len(rol_user) == 0:  
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def login_required_member(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si la cookie 'identificacion' está presente
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre ='Miembro'", (identificacion))
            rol_user = cursor.fetchall()
            print(rol_user, "ROOOOOL DEL USUARIO")
            if len(rol_user) == 0:  # Si no hay cookie, redirige al login
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required_coach(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            print(f"Identificación de la cookie: {identificacion}")  
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre = 'Entrenador'", (identificacion))
            rol_user = cursor.fetchall()
            print(f"Rol del usuario: {rol_user}") 
            if len(rol_user) == 0:  # Si no hay rol "Entrenador", redirigir al login
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            print("Cookie de identificación no encontrada. Redirigiendo al login.")
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function

def login_required_receptionist(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        identificacion = request.cookies.get('identificacion')
        if identificacion:
            print(f"Identificación de la cookie: {identificacion}")
            cursor.execute("SELECT r.nombre FROM bd_gimnasio2.usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s AND r.nombre = 'Recepcionista'", (identificacion))
            rol_user = cursor.fetchall()
            print(f"Rol del usuario: {rol_user}")
            if len(rol_user) == 0:
                print("Usuario no autenticado. Redirigiendo al login.")
                return redirect(url_for('login'))
        else:
            print("Cookie de identificación no encontrada. Redirigiendo al login.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#--GUARDAR LA COKKIE


#OBTENER EL LISTADO DE MIEMBROS PARA GESTION
def lista_miembros():
    cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, u.edad, u.correo, u.telefono, r.nombre FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol")
    listado_miembros = cursor.fetchall()
    return listado_miembros
#OBTENER EL LISTADO DE MIEMBROS

#OBTENER LISTA DE LOS PROVEEDORES
def lista_proveedores():
    cursor.execute("SELECT * FROM proveedor")
    listado_proveedores = cursor.fetchall()
    return listado_proveedores
#OBTENER LISTA DE LOS PROVEEDORES

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
    cursor.execute("SELECT COUNT(*) AS listado_clases FROM clase")
    result_lista_reservas = cursor.fetchone()[0]
    return result_lista_reservas

def listado_empleados():
    cursor.execute("SELECT u.id_usuario, u.identificacion, u.nombre, u.apellido, r.nombre, r.salario FROM usuario u JOIN rol r ON u.id_rol = r.id_rol WHERE r.nombre <> 'Miembro';")
    result_emple = cursor.fetchall()
    print(f"esto es lo que llega {result_emple} ")
    return result_emple

#OBTENER LA CANTIDAD DE ROLES

#--AGREGAR USUARIO
def add_user(identificacion, nombre, apellido, edad, correo, telefono, genero, plan_trab, rol, contrasena, horario):
    try:
        # 1. Insertar en la tabla usuario
        cursor.execute("""
            INSERT INTO usuario (
                identificacion, nombre, apellido, edad, correo, telefono, id_genero, id_plan_trabajo, id_rol, contrasena
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (identificacion, nombre, apellido, edad, correo, telefono, genero, plan_trab, rol, contrasena))
        
        connection.commit()

        # 2. Obtener el id del usuario recién insertado
        cursor.execute("SELECT id_usuario FROM usuario WHERE identificacion = %s", (identificacion,))
        user = cursor.fetchone()

        if user:
            id_usuario = user[0]

            # 3. Si se seleccionó un horario y es entrenador (por ejemplo, rol == 2), insertar en horario_entrenador
            if horario and str(rol) == "2":  # Ajusta el ID del rol si es necesario
                cursor.execute("""
                    INSERT INTO horario_entrenador (id_usuario, id_horario) VALUES (%s, %s)
                """, (id_usuario, horario))
                connection.commit()

        return True

    except Exception as e:
        print("Error al agregar usuario:", e)
        print("Datos recibidos:", identificacion, nombre, apellido, edad, correo, telefono, genero, plan_trab, rol, contrasena, horario)
        return False

#--AGREGAR USUARIO

#BUSQUEDA DE USUARIOS
def search_users(identificacion):
    cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, u.edad, u.correo, u.telefono, g.tipo AS genero, p.nombre AS plan_trabajo, r.nombre AS rol FROM usuario u INNER JOIN genero g ON u.id_genero = g.id_genero INNER JOIN plan_trabajo p ON u.id_plan_trabajo = p.id_plan_trabajo INNER JOIN rol r ON u.id_rol = r.id_rol WHERE u.identificacion = %s", (identificacion))
    result_busqueda = cursor.fetchall()
    return result_busqueda

#ASIGNACION DE MEMBRESIAS
def assig_membreships():
    try:
        cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, u.id_usuario FROM usuario u LEFT JOIN membresia_usuario mu ON mu.id_usuario = u.id_usuario WHERE u.id_rol = 5 AND mu.id_membresia_usuario IS NULL")
        campos_asignacion = cursor.fetchall()
        print(f'esto es lo que llega de asignacion de membresia')
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
        return False 
    
#ESTADO DE LA MEMBRESIA
def status_membreship():
    cursor.execute("SELECT id_estado_membresia, nombre FROM estado_membresia")
    status = cursor.fetchall()
    return status

def horario_empleado():
    cursor.execute("SELECT id_horario, nombre, descripcion FROM horario")
    horarios = cursor.fetchall()
    return horarios

#ACTUALIZAR MEMBRESIA
def obtener_usuarios_con_membresia():
    cursor.execute("""
        SELECT 
            u.identificacion, 
            u.nombre, 
            u.apellido, 
            mu.id_membresia, 
            mu.fecha_inicio, 
            mu.fecha_fin, 
            mu.id_estado_membresia, 
            mu.id_membresia_usuario,
            u.id_usuario
        FROM usuario u
        INNER JOIN membresia_usuario mu ON mu.id_usuario = u.id_usuario
        WHERE u.id_rol = 5 AND mu.id_membresia_usuario IS NOT NULL
    """)
    resultados = cursor.fetchall()
    return [list(row) for row in resultados]


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
    cursor.execute("""
        SELECT 
            m.nombre            AS nombre_maquina,
            i.serial            AS serial,
            i.fecha_compra,
            i.precio,
            p.nombre            AS proveedor,
            i.disponibilidad,
            i.id_inventario_maquina,
            r.id_estado_revision,
            orv.observacion_admin,
            orv.observacion_tecnico
        FROM inventario_maquina i
        INNER JOIN maquina m ON i.id_maquina = m.id_maquina
        INNER JOIN proveedor p ON i.id_proveedor = p.id_proveedor
        LEFT JOIN revision r 
            ON r.id_inventario_maquina = i.id_inventario_maquina
            AND r.id_revision = (
                SELECT MAX(r2.id_revision)
                FROM revision r2
                WHERE r2.id_inventario_maquina = i.id_inventario_maquina
            )
        LEFT JOIN observacion_revision orv 
            ON orv.id_revision = r.id_revision
        ORDER BY i.id_inventario_maquina;
    """)
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
    print("Usuario con maquina reservada:", result_busqueda)
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

def guardar_acceso(tipo_acceso, id_usuario):
    try:
        if tipo_acceso == "Active":
            cursor.execute("""
                INSERT INTO acceso (fecha_inicio, tipo_acceso, id_usuario, duracion)
                VALUES (NOW(), %s, %s, DEFAULT)
            """, (tipo_acceso, id_usuario))
        else:
            # Buscar el último acceso activo de este usuario
            cursor.execute("""
                SELECT id_acceso, fecha_inicio 
                FROM acceso 
                WHERE id_usuario = %s AND tipo_acceso = 'Active'
                ORDER BY fecha_inicio DESC LIMIT 1
            """, (id_usuario,))
            acceso = cursor.fetchone()

            if acceso:
                id_acceso, fecha_inicio = acceso
                cursor.execute("""
                    UPDATE acceso 
                    SET fecha_fin = NOW(),
                        tipo_acceso = %s,
                        duracion = TIMEDIFF(NOW(), fecha_inicio)
                    WHERE id_acceso = %s
                """, (tipo_acceso, id_acceso))

        connection.commit()
        return True
    except Exception as e:
        print("Error al guardar acceso:", e)
        return False


# --- Función de servicio (consulta y actualización en la BD) ---
def finalizar_acceso(id_usuario):
    try:
        # 1. Buscar el último acceso activo del usuario
        cursor.execute("""
            SELECT id_acceso, fecha_inicio 
            FROM acceso
            WHERE id_usuario = %s AND tipo_acceso = 'Active'
            ORDER BY fecha_inicio DESC
            LIMIT 1
        """, (id_usuario,))
        acceso = cursor.fetchone()

        if not acceso:
            cursor.close()
            return {'error': 'No hay acceso activo para este usuario'}

        id_acceso, fecha_inicio = acceso

        # 2. Actualizar con fecha_fin y duración
        cursor.execute("""
            UPDATE acceso
            SET fecha_fin = NOW(),
                duracion = TIMEDIFF(NOW(), fecha_inicio),
                tipo_acceso = 'Inactive'
            WHERE id_acceso = %s
        """, (id_acceso,))

        connection.commit()
        cursor.close()

        return {'message': 'Acceso finalizado correctamente'}

    except Exception as e:
        print("Error en finalizar_acceso_db:", e)
        return {'error': str(e)}


def consultar_acceso_usuario(id_usuario):
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)  # DictCursor devuelve diccionario

        cursor.execute("""
            SELECT tipo_acceso, fecha_inicio, fecha_fin
            FROM acceso
            WHERE id_usuario = %s
            ORDER BY fecha_inicio DESC
            LIMIT 1
        """, (id_usuario,))
        acceso = cursor.fetchone()

        if acceso is None:
            return {'tipo_acceso': 'Inactive'}

        return acceso

    except Exception as e:
        return {'error': f'Error al obtener acceso: {str(e)}'}

from pymysql.cursors import DictCursor

def cambiar_estado_acceso_db(id_usuario):
    try:
        cursor = connection.cursor(DictCursor)

        # 1️⃣ Buscar acceso activo
        cursor.execute("""
            SELECT id_acceso, fecha_inicio
            FROM acceso
            WHERE id_usuario = %s AND tipo_acceso = 'Active' AND fecha_fin IS NULL
            ORDER BY fecha_inicio DESC LIMIT 1
        """, (id_usuario,))
        acceso_actual = cursor.fetchone()

        if acceso_actual is None:
            return {'error': f"No se encontró acceso activo para el usuario ID: {id_usuario}."}

        # 2️⃣ Cerrar acceso (cambia estado y fecha_fin)
        cursor.execute("""
            UPDATE acceso
            SET tipo_acceso = 'Inactive', fecha_fin = NOW()
            WHERE id_acceso = %s
        """, (acceso_actual['id_acceso'],))
        connection.commit()

        # 3️⃣ Calcular duración en segundos
        cursor.execute("""
            SELECT TIMESTAMPDIFF(SECOND, fecha_inicio, fecha_fin) AS duracion_segundos
            FROM acceso WHERE id_acceso = %s
        """, (acceso_actual['id_acceso'],))
        segundos = cursor.fetchone()['duracion_segundos']

        # 4️⃣ Convertir duración a HH:MM:SS
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos = segundos % 60
        duracion_legible = f"{horas:02}:{minutos:02}:{segundos:02}"

        # 5️⃣ Guardar duración en la tabla
        cursor.execute("""
            UPDATE acceso
            SET duracion = %s
            WHERE id_acceso = %s
        """, (duracion_legible, acceso_actual['id_acceso']))
        connection.commit()

        return {
            'message': 'Estado de acceso cambiado a Inactive exitosamente.',
            'duracion': duracion_legible
        }

    except Exception as e:
        return {'error': f'Error al cambiar el estado del acceso: {str(e)}'}



#ASIGNAR ENTRENADOR
# def asignar_supervision_db(id_acceso_miembro, id_usuario_miembro):
#     try:
#         cursor = connection.cursor(DictCursor)

#         # 1️⃣ Obtener el plan del miembro
#         cursor.execute("""
#             SELECT id_plan_trabajo
#             FROM usuario
#             WHERE id_usuario = %s
#         """, (id_usuario_miembro,))
#         miembro = cursor.fetchone()

#         if not miembro or not miembro['id_plan_trabajo']:
#             return {'error': 'El miembro no tiene plan de trabajo asignado.'}

#         id_plan_trabajo = miembro['id_plan_trabajo']

#         # 2️⃣ Buscar un entrenador con el mismo plan y acceso activo
#         cursor.execute("""
#             SELECT a.id_acceso, u.id_usuario, u.nombre, u.apellido
#             FROM usuario u
#             JOIN acceso a ON u.id_usuario = a.id_usuario
#             WHERE u.id_plan_trabajo = %s
#               AND u.id_rol = 2   -- rol entrenador
#               AND a.tipo_acceso = 'Active'
#               AND a.fecha_fin IS NULL
#             LIMIT 1
#         """, (id_plan_trabajo,))
#         entrenador = cursor.fetchone()

#         if not entrenador:
#             return {'error': 'No hay entrenadores disponibles en este momento.'}

#         id_acceso_entrenador = entrenador['id_acceso']

#         # 3️⃣ Insertar en supervision
#         cursor.execute("""
#             INSERT INTO supervision (id_acceso_miembro, id_acceso_entrenador)
#             VALUES (%s, %s)
#         """, (id_acceso_miembro, id_acceso_entrenador))
#         connection.commit()

#         return {
#             'message': f"Supervisión asignada con el entrenador {entrenador['nombre']} {entrenador['apellido']}",
#             'id_acceso_miembro': id_acceso_miembro,
#             'id_acceso_entrenador': id_acceso_entrenador
#         }

#     except Exception as e:
#         return {'error': f'Error al asignar supervisión: {str(e)}'}

# def asignar_entrenador():
#     cursor.execute("SELECT u.identificacion, u.nombre, u.apellido, a.id_acceso, a.tipo_acceso, a.fecha, r.nombre AS nombre_rol, u.id_usuario, pt.nombre FROM acceso a INNER JOIN usuario u ON a.id_usuario = u.id_usuario INNER JOIN rol r ON u.id_rol = r.id_rol INNER JOIN plan_trabajo pt ON pt.id_plan_trabajo = u.id_plan_trabajo  WHERE r.nombre IN ('Miembro', 'Entrenador') AND a.tipo_acceso = 'Active' AND DATE(a.fecha) = CURDATE();")
#     resultado = cursor.fetchall()
#     print('ESTE ES EL RESULTADO DE LA CONSULTA')
#     print(resultado)
#     return resultado

# Obtener datos del entrenador (id_usuario, id_plan y horario)
def obtener_entrenador(id_entrenador, cursor):
    query = """
        SELECT id_usuario, id_plan, horario
        FROM empleados
        WHERE id_usuario = %s
    """
    cursor.execute(query, (id_entrenador,))
    return cursor.fetchone()  # Retorna un dict o tupla


# Obtener miembros que tengan el mismo plan del entrenador
def obtener_miembros_por_plan(id_plan, cursor):
    query = """
        SELECT id_usuario
        FROM miembros
        WHERE id_plan = %s
    """
    cursor.execute(query, (id_plan,))
    return cursor.fetchall()  # Lista de miembros


# Insertar la supervisión (relación entrenador - miembro)
def asignar_supervision(id_entrenador, id_miembro, fecha, cursor, connection):
    query = """
        INSERT INTO supervision (id_entrenador, id_miembro, fecha)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (id_entrenador, id_miembro, fecha))
    connection.commit()

def obtener_usuarios_activos(cursor):
    query = """
        SELECT u.id_usuario, u.nombre, u.apellido, u.correo, a.tipo_acceso, a.fecha_inicio, u.rol, u.estado, u.id_plan
        FROM usuario u
        LEFT JOIN acceso a ON u.id_usuario = a.id_usuario
        WHERE a.tipo_acceso = 'Active' AND u.estado = 'Activo'
    """
    cursor.execute(query)
    return cursor.fetchall()

def asignar_entrenador():
    try:
        cursor = connection.cursor()
        query = """
            SELECT u.id_usuario, u.nombre, u.apellido, u.correo,
                   a.tipo_acceso, a.fecha_inicio, r.nombre AS rol, u.id_plan_trabajo
            FROM usuario u
            LEFT JOIN acceso a ON u.id_usuario = a.id_usuario
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE a.tipo_acceso = 'Active'
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        return [list(row) for row in resultados]
    except Exception as e:
        return {'error': f'Error en asignar_entrenador: {str(e)}'}

#MIEMBRO
#OBTENER PLAN DE TRABAJO DEL MIEMBRO
def obtener_plan_trabajo(identificacion):
    cursor.execute(
        "SELECT p.nombre FROM usuario u INNER JOIN plan_trabajo p ON u.id_plan_trabajo = p.id_plan_trabajo WHERE u.identificacion = %s", 
        (identificacion,))
    plan = cursor.fetchone()
    return plan[0] if plan else None  

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

# Función para guardar la clase en la base de datos ADMINISTRADOR
def save_class_to_db(nombre, fecha_inicio, hora, duration):
    try:
        cursor.execute('INSERT INTO clase (nombre, fecha_inicio, hora, duracion) VALUES (%s, %s, %s, %s)', (nombre, fecha_inicio, hora, duration))
        connection.commit()
        return {'success': True, 'message': 'Clase guardada exitosamente'}
    except pymysql.MySQLError as e:
        return {'success': False, 'message': f'Error al guardar en la base de datos: {e}'}

#FUNCION PARA ELIMINAR CLASES
def list_class():
    cursor.execute('SELECT * FROM clase')
    resul_list_class = cursor.fetchall()
    return resul_list_class

def delete_class(id_clase):
    try:
        cursor.execute('DELETE FROM clase WHERE id_clase = %s', (id_clase,))
        connection.commit()
        return {'success': True, 'message': 'Clase eliminada exitosamente'}
    except pymysql.MySQLError as e:
        return {'success': False, 'message': f'Error al modificar la base de datos: {e}'}


#Reserva de clase usuario
def reservation_class():
    return True

#Conteo de maquinas inventariadas
def cant_maquinas():
    cursor.execute("SELECT COUNT(*) AS listado_maquinas FROM inventario_maquina")
    resul_lista_maquinas = cursor.fetchone()[0]
    return resul_lista_maquinas

#Obtener maquinas
def get_maquinas():
    cursor.execute("SELECT id_maquina, nombre FROM maquina")
    maquinas = [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
    return jsonify(maquinas)

#Obtener las reservas de las maquinas de hoy
def obtener_reservas_maquinas():
    cursor.execute('''
        SELECT rm.fecha, rm.hora_inicio, rm.hora_fin, u.nombre, u.apellido, m.nombre AS nombre_maquina
        FROM maquina m 
        JOIN inventario_maquina im ON m.id_maquina = im.id_maquina
        JOIN reserva_maquina rm ON im.id_inventario_maquina = rm.id_inventario_maquina
        JOIN membresia_usuario mu ON rm.id_membresia_usuario = mu.id_membresia_usuario
        JOIN usuario u ON mu.id_usuario = u.id_usuario 
        WHERE rm.fecha = CURDATE()
        ORDER BY rm.hora_inicio;
    ''')
    resultados = cursor.fetchall()
    return [
        {
            "nombre_maquina": fila[5],
            "nombre": fila[3],
            "apellido": fila[4],
            "fecha": str(fila[0]),  
            "hora_inicio": str(fila[1]),
            "hora_fin": str(fila[2]),
            "disponibilidad": "Reservada"
        }
        for fila in resultados
    ]



#Obtiene las maquinas que no tienen reserva
def obtener_maquinas_disponibles():
    cursor.execute('''
        SELECT m.nombre AS nombre_maquina, COUNT(rm.id_reserva) AS reservas
        FROM maquina m
        LEFT JOIN inventario_maquina im ON m.id_maquina = im.id_maquina
        LEFT JOIN reserva_maquina rm 
            ON im.id_inventario_maquina = rm.id_inventario_maquina 
            AND rm.fecha = CURDATE()
        GROUP BY m.id_maquina
        ORDER BY m.nombre;
    ''')
    resultados = cursor.fetchall()
    return [
        {
            "nombre_maquina": fila[0],
            "reservas_hoy": fila[1],
            "total_turnos": 40,
            "disponibilidad": "Disponible" if fila[1] < 40 else "No disponible"
        }
        for fila in resultados
    ]

#reservas que hay hoy
def consultar_reservas_de_hoy():
    cursor.execute('''
        SELECT m.id_maquina, m.nombre, rm.hora_inicio
        FROM maquina m
        LEFT JOIN inventario_maquina im ON m.id_maquina = im.id_maquina
        LEFT JOIN reserva_maquina rm ON im.id_inventario_maquina = rm.id_inventario_maquina
            AND rm.fecha = CURDATE()
    ''')
    return cursor.fetchall()

#Obtener cantidad de instructores
def cant_proveedores():
    cursor.execute("SELECT COUNT(*) AS listado_proveedores FROM proveedor")
    resul_lista_proveedor = cursor.fetchone()[0]
    return resul_lista_proveedor

#Obtener cantidad de empleados
def cant_empleados():
    cursor.execute("SELECT COUNT(*) AS listado_empleados FROM usuario WHERE id_rol <>5")
    result_lista_empleados = cursor.fetchone()[0]
    return result_lista_empleados


#RESERVAS DE MAQUINAS
def obtener_maquinas_disponibles_para_reserva():
    cursor.execute('''
        SELECT im.id_inventario_maquina, m.nombre
        FROM maquina m
        JOIN inventario_maquina im ON m.id_maquina = im.id_maquina
        LEFT JOIN reserva_maquina rm ON im.id_inventario_maquina = rm.id_inventario_maquina
            AND rm.fecha = CURDATE()
        WHERE rm.id_reserva IS NULL
    ''')
    return cursor.fetchall()


def verificar_reserva(id_maquina, hora):
    cursor.execute("""
        SELECT COUNT(*) FROM reserva_maquina
        WHERE id_maquina = %s AND hora_inicio = %s AND fecha = CURDATE()
    """, (id_maquina, hora))
    resultado = cursor.fetchone()
    return resultado[0] > 0

def registrar_reserva(id_membresia_usuario, id_inventario_maquina, hora_inicio, hora_fin):
    try:
        print("Intentando insertar:")
        print("Membresía usuario:", id_membresia_usuario)
        print("Máquina (inventario):", id_inventario_maquina)
        print("Hora inicio:", hora_inicio)
        print("Hora fin:", hora_fin)

        cursor.execute("""
            INSERT INTO reserva_maquina (id_membresia_usuario, id_inventario_maquina, fecha, hora_inicio, hora_fin)
            VALUES (%s, %s, CURDATE(), %s, %s)
        """, (id_membresia_usuario, id_inventario_maquina, hora_inicio, hora_fin))
        
        connection.commit()
        print("Reserva insertada correctamente.")
        
        return {'success': True, 'message': '¡Reserva registrada con éxito!'}
    
    except pymysql.MySQLError as e:
        print("Error en MySQL:", e)
        return {'success': False, 'message': f'Error al guardar en la base de datos: {e}'}


    
def existe_reserva_en_bloque(id_maquina, hora_inicio):
    if len(hora_inicio) == 5:
        hora_inicio += ":00"

    print(f"[Verificación reserva existente] Máquina: {id_maquina}, Hora: {hora_inicio}")

    cursor.execute("""
        SELECT 1 FROM reserva_maquina
        WHERE id_inventario_maquina = %s
          AND hora_inicio = %s
          AND fecha = CURDATE()
    """, (id_maquina, hora_inicio))

    return cursor.fetchone() is not None








#Obtener membresia del usuario
def obtener_id_membresia_usuario(identificacion):
    cursor.execute('''
        SELECT mu.id_membresia_usuario
        FROM usuario u
        JOIN membresia_usuario mu ON u.id_usuario = mu.id_usuario
        WHERE u.identificacion = %s AND mu.id_estado_membresia = 1
        ORDER BY mu.fecha_inicio DESC
        LIMIT 1
    ''', (identificacion,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return None


#Verificar que no tenga una reserva de la maquina seguida
def consultar_bloques_contiguos(id_membresia_usuario, hora_inicio):
    try:
        hora_actual = datetime.strptime(hora_inicio, "%H:%M:%S")
    except ValueError:
        hora_actual = datetime.strptime(hora_inicio[:5], "%H:%M")

    hora_anterior = (hora_actual - timedelta(minutes=15)).strftime("%H:%M:%S")
    hora_siguiente = (hora_actual + timedelta(minutes=15)).strftime("%H:%M:%S")

    cursor.execute("""
        SELECT * FROM reserva_maquina
        WHERE id_membresia_usuario = %s AND hora_inicio IN (%s, %s) AND fecha = CURDATE()
    """, (id_membresia_usuario, hora_anterior, hora_siguiente))

    return cursor.fetchone()

def registrar_pago_nomina(datos):
    try:
        cursor.execute("""
            INSERT INTO nomina (
                id_usuario, fecha_generacion, salario_base, 
                auxilio_transporte, aporte_salud, aporte_pension,
                total_devengado, total_deducciones, liquido_a_recibir
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, datos)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error al registrar la nómina: {e}")
        return False
    
def obtener_id_usuario_por_identificacion(identificacion):
    cursor.execute("SELECT id_usuario FROM usuario WHERE identificacion = %s", (identificacion,))
    result = cursor.fetchone()
    return result[0] if result else None

#GESTINAR LOS PROVEEDORES
def insertar_proveedor(nombre):
    try:
        cursor.execute("""
            INSERT INTO proveedor (
                       nombre) VALUES (%s)
                       """, nombre)
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error al registrar el proveedor {e}")
        return False
    
def eliminar_proveedor_id(id_proveedor):
    try:
        cursor.execute("DELETE FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        connection.commit()
        print(f"Proveedor {id_proveedor} eliminado correctamente.")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error al eliminar el proveedor: {e}")
        return False

    
def actualizar_proveedor(id_proveedor, nombre):
    try:
        cursor.execute("UPDATE proveedor SET nombre = %s WHERE id_proveedor = %s", (nombre, id_proveedor))
        connection.commit()
        print(f"Proveedor {id_proveedor} actualizado correctamente.")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error al actualizar los proveedores: {e}")
        return False

def obtener_proveedor_por_id(id_proveedor):
    try:
        cursor.execute("SELECT id_proveedor, nombre FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        resultado = cursor.fetchone()
        return resultado 
    except Exception as e:
        print(f"Error al obtener proveedor por ID: {e}")
        return None

#FIN GESTION DE PROVEEDORES

#RESERVA DE LAS CLASES
def obtener_clases_disponibles():
    cursor.execute("""
        SELECT id_clase, nombre, fecha_inicio, hora, duracion
        FROM clase
    """)
    return cursor.fetchall()


def obtener_clase_por_id(id_clase):
    cursor.execute("""
        SELECT id_clase, nombre, fecha_inicio, hora, duracion
        FROM clase
        WHERE id_clase = %s
    """, (id_clase,))
    return cursor.fetchone()


def reservar_clase(id_clase, id_membresia_usuario):
    try:
        cursor.execute("""
            INSERT INTO reserva_clase (fecha, hora, id_clase, id_membresia_usuario)
            VALUES (DATE('now'), TIME('now'), ?, ?)
        """, (id_clase, id_membresia_usuario))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error al reservar clase: {e}")
        return False
    
def obtener_id_membresia_usuario_activa(id_usuario):
    cursor.execute("""
        SELECT id_membresia_usuario 
        FROM membresia_usuario
        WHERE id_usuario = %s AND id_estado_membresia = 1
        LIMIT 1
    """, (id_usuario,))
    
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

def insertar_reserva_clase(fecha, hora, id_clase, id_membresia_usuario):
    cursor.execute("""
            INSERT INTO reserva_clase (fecha, hora, id_clase, id_membresia_usuario)
            VALUES (%s, %s, %s, %s)
        """, (fecha, hora, id_clase, id_membresia_usuario))
    connection.commit()
    
    return True

def existe_reserva(id_clase, id_membresia_usuario, fecha, hora):
    cursor.execute("""
        SELECT 1 FROM reserva_clase
        WHERE id_clase = %s AND id_membresia_usuario = %s AND fecha = %s AND hora = %s
        LIMIT 1
    """, (id_clase, id_membresia_usuario, fecha, hora))
    resultado = cursor.fetchone()
    return resultado is not None

def obtener_reservas_usuario(id_usuario):
    cursor.execute("""
        SELECT rc.fecha, rc.hora, c.nombre
        FROM reserva_clase rc
        JOIN membresia_usuario mu ON rc.id_membresia_usuario = mu.id_membresia_usuario
        JOIN clase c ON rc.id_clase = c.id_clase
        WHERE mu.id_usuario = %s
        ORDER BY rc.fecha, rc.hora
    """, (id_usuario,))
    return cursor.fetchall()

def obtener_id_clase_por_nombre(nombre_clase):
    cursor.execute("""
        SELECT id_clase FROM clase
        WHERE nombre = %s
    """, (nombre_clase,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def cancelar_reserva_en_bd(id_clase, id_membresia_usuario, fecha, hora):
    cursor.execute("""
        DELETE FROM reserva_clase
        WHERE id_clase = %s AND id_membresia_usuario = %s AND fecha = %s AND hora = %s
    """, (id_clase, id_membresia_usuario, fecha, hora))
    connection.commit()

def datos_miembro(id_usuario):
    cursor.execute('''
        SELECT 
            u.id_usuario, 
            u.identificacion, 
            u.nombre, 
            u.apellido, 
            u.edad, 
            u.correo, 
            u.telefono, 
            u.contrasena, 
            g.tipo, 
            u.id_plan_trabajo, 
            u.id_rol 
        FROM 
            usuario u 
        JOIN 
            rol r ON u.id_rol = r.id_rol  JOIN genero g ON u.id_genero = g.id_genero
        WHERE 
            u.id_usuario = %s AND r.nombre = 'Miembro'
    ''', (id_usuario,))
    
    resultado = cursor.fetchone()
    return resultado

def actualizar_datos_miembro(id_usuario, nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash=None):
    if contrasena_hash:
        cursor.execute("""
            UPDATE usuario
            SET nombre = %s,
                apellido = %s,
                identificacion = %s,
                edad = %s,
                correo = %s,
                telefono = %s,
                contrasena = %s
            WHERE id_usuario = %s
        """, (nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash, id_usuario))
    else:
        cursor.execute("""
            UPDATE usuario
            SET nombre = %s,
                apellido = %s,
                identificacion = %s,
                edad = %s,
                correo = %s,
                telefono = %s
            WHERE id_usuario = %s
        """, (nombre, apellido, identificacion, edad, correo, telefono, id_usuario))
    connection.commit()
    return True


#FIN RESERVA DE LAS CLASES

#ENTRENADOR
def obtener_clientes_sin_avance_hoy(id_entrenador):
    hoy = date.today()
    cursor.execute("""
        SELECT m.id_usuario, m.identificacion, m.nombre, m.apellido, m.correo, m.telefono, p.nombre AS plan_trabajo
        FROM usuario e
        JOIN usuario m 
            ON e.id_plan_trabajo = m.id_plan_trabajo
        JOIN plan_trabajo p 
            ON m.id_plan_trabajo = p.id_plan_trabajo
        WHERE e.id_usuario = %s
        AND m.id_rol = (SELECT id_rol FROM rol WHERE nombre = 'Miembro')
        AND m.id_usuario <> e.id_usuario
        AND m.id_usuario NOT IN (
            SELECT id_usuario_miembro
            FROM progreso_trabajo
            WHERE id_usuario_entrenador = %s
            AND DATE(fecha) = %s
        )
    """, (id_entrenador, id_entrenador, hoy))
    return cursor.fetchall()

def existe_avance_hoy(id_usuario_miembro, id_entrenador):
    hoy = date.today()
    cursor.execute("""
        SELECT 1 
        FROM progreso_trabajo 
        WHERE id_usuario_miembro = %s 
        AND id_usuario_entrenador = %s 
        AND DATE(fecha) = %s
    """, (id_usuario_miembro, id_entrenador, hoy))
    resultado = cursor.fetchone()
    return resultado is not None


def insertar_progreso(peso, descripcion, fecha, id_miembro, id_entrenador):
    cursor.execute("""
        INSERT INTO progreso_trabajo (peso, descripcion, fecha, id_usuario_miembro, id_usuario_entrenador)
        VALUES (%s, %s, %s, %s, %s)
    """, (peso, descripcion, fecha, id_miembro, id_entrenador))
    connection.commit()
    return True

def obtener_historial_avances(id_entrenador):
    cursor.execute("""
        SELECT m.nombre, m.apellido, p.peso, p.descripcion, p.fecha
        FROM progreso_trabajo p
        JOIN usuario m ON p.id_usuario_miembro = m.id_usuario
        WHERE p.id_usuario_entrenador = %s
        ORDER BY p.fecha DESC
    """, (id_entrenador,))
    return cursor.fetchall()

# def datos_entrenador(id_usuario):
#     cursor.execute('''
#         SELECT 
#             u.id_usuario, 
#             u.identificacion, 
#             u.nombre, 
#             u.apellido, 
#             u.edad, 
#             u.correo, 
#             u.telefono, 
#             u.contrasena, 
#             g.tipo, 
#             u.id_plan_trabajo, 
#             u.id_rol 
#         FROM 
#             usuario u 
#         JOIN 
#             rol r ON u.id_rol = r.id_rol  JOIN genero g ON u.id_genero = g.id_genero
#         WHERE 
#             u.id_usuario = %s AND r.nombre = 'Entrenador'
#     ''', (id_usuario,))
    
#     resultado = cursor.fetchone()
#     return resultado

# def actualizar_datos_entrenador(id_usuario, nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash=None):
#     if contrasena_hash:
#         cursor.execute("""
#             UPDATE usuario
#             SET nombre = %s,
#                 apellido = %s,
#                 identificacion = %s,
#                 edad = %s,
#                 correo = %s,
#                 telefono = %s,
#                 contrasena = %s
#             WHERE id_usuario = %s
#         """, (nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash, id_usuario))
#     else:
#         cursor.execute("""
#             UPDATE usuario
#             SET nombre = %s,
#                 apellido = %s,
#                 identificacion = %s,
#                 edad = %s,
#                 correo = %s,
#                 telefono = %s
#             WHERE id_usuario = %s
#         """, (nombre, apellido, identificacion, edad, correo, telefono, id_usuario))
#     connection.commit()
#     return True


#ENVIAR LA MAQUINA PARA LA REVISION 
def maquinas_sin_disponibles():
    cursor.execute("""
        SELECT 
    i.id_inventario_maquina,
    m.nombre       AS nombre_maquina,
    i.serial       AS serial_maquina,
    i.fecha_compra,
    i.precio,
    p.nombre       AS proveedor,
    i.disponibilidad
FROM inventario_maquina i
INNER JOIN maquina m ON i.id_maquina = m.id_maquina
INNER JOIN proveedor p ON i.id_proveedor = p.id_proveedor
WHERE i.disponibilidad = 0;

    """)
    maquinas = cursor.fetchall()
    return maquinas

def lista_tecnicos(id_usuario= None):
    if id_usuario:
        cursor.execute("SELECT u.id_usuario, u.identificacion, u.nombre, u.apellido, u.correo, r.nombre, u.edad, g.tipo FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol INNER JOIN genero g ON g.id_genero = u.id_genero WHERE r.nombre = 'Tecnico' AND u.id_usuario = %s", (id_usuario))
        resultado = cursor.fetchone()
        return resultado
    else:
        cursor.execute("SELECT u.id_usuario, u.nombre, u.apellido, u.identificacion, u.correo, r.nombre AS rol, u.edad, u.id_genero FROM usuario u INNER JOIN rol r ON u.id_rol = r.id_rol WHERE r.nombre = 'Tecnico'")
        resultado = cursor.fetchone()
        return resultado

def actualizar_usuario(id, nombre, apellido, correo,  edad,  telefono, contrasena):
    cursor.execute("""
        UPDATE usuario 
        SET nombre=%s, apellido=%s, correo=%s,  edad=%s, telefono=%s, contrasena=%s
        WHERE id_usuario=%s
    """, (nombre, apellido, correo, edad, telefono, contrasena, id))
    connection.commit()






def insert_revision_sql():
    return """
        INSERT INTO revision (fecha_revision, id_inventario_maquina, id_estado_revision, id_usuario)
        VALUES (NOW(), %s, %s, %s)
    """

def insert_observacion_sql():
    return """
        INSERT INTO observacion_revision (id_revision, id_usuario, observacion_admin, fecha)
        VALUES (%s, %s, %s, NOW())
    """

def last_id_sql():
    return "SELECT LAST_INSERT_ID() AS id_revision"



# FUNCIONES DE INSERCIÓN
def insertar_revision(id_inventario_maquina, id_usuario, observacion_admin, estado):
    try:
        conn = connection
        cursor.execute(insert_revision_sql(), (id_inventario_maquina, estado, id_usuario))
        cursor.execute(last_id_sql())
        id_revision = cursor.fetchone()[0]
        cursor.execute(insert_observacion_sql(), (id_revision, id_usuario, observacion_admin))
        conn.commit()

        return id_revision

    except Exception as e:
        conn.rollback()
        print(f"Error al insertar revisión: {e}")
        return None

def reports_machine():
    cursor.execute("SELECT i.id_maquina, m.nombre, r.fecha_revision, r.id_estado_revision, o.observacion_admin, o.observacion_tecnico FROM inventario_maquina i JOIN maquina m ON i.id_maquina = m.id_maquina JOIN revision r ON i.id_inventario_maquina = r.id_inventario_maquina LEFT JOIN observacion_revision o ON o.id_revision = r.id_revision")
    reportes = cursor.fetchall()
    return reportes

#ACTUALIZAR EL ESTADO DE LA REVISION DE LA MAQUINA DESDE EL PERFIL DE TECNICO
def actualizar_estado_revision(id_revision, estado):
    cursor.execute("UPDATE revision SET id_estado_revision = %s WHERE id_revision = %s", (estado, id_revision))
    connection.commit()
    return True
    
def insertar_observacion(id_revision, id_usuario, observacion):
    cursor.execute("SELECT id_obs_revision FROM observacion_revision WHERE id_revision = %s", (id_revision,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute("""
            UPDATE observacion_revision
            SET observacion_tecnico = %s, fecha = NOW(), id_usuario = %s
            WHERE id_revision = %s
        """, (observacion, id_usuario, id_revision))

    else:
        cursor.execute("""
            INSERT INTO observacion_revision (id_revision, id_usuario, observacion_tecnico, fecha)
            VALUES (%s, %s, %s, NOW())
        """, (id_revision, id_usuario, observacion))

    connection.commit()


def obtener_revision(id_revision):
    cursor.execute("SELECT r.id_revision, r.fecha_revision, r.id_estado_revision, m.nombre FROM revision r JOIN inventario_maquina i ON r.id_inventario_maquina = i.id_inventario_maquina INNER JOIN maquina m ON m.id_maquina = i.id_maquina WHERE r.id_revision = %s", (id_revision,))
    revision = cursor.fetchone()
    return revision

def obtener_observaciones(id_revision):
    cursor.execute("""
        SELECT observacion_admin, observacion_tecnico, fecha
        FROM observacion_revision
        WHERE id_revision = %s
        ORDER BY fecha DESC
    """, (id_revision,))
    observaciones = cursor.fetchall()
    return observaciones

def actualizar_estado_revision(id_revision, nuevo_estado):
    cursor.execute("""
        UPDATE revision
        SET id_estado_revision = %s
        WHERE id_revision = %s
    """, (nuevo_estado, id_revision))
    connection.commit()


def obtener_revisiones_pendientes():
    cursor.execute("""
        SELECT r.id_revision, r.fecha_revision, r.id_estado_revision,
               i.id_maquina, m.nombre AS maquina,
               o.observacion_admin
        FROM inventario_maquina i
        JOIN maquina m ON i.id_maquina = m.id_maquina
        JOIN revision r ON i.id_inventario_maquina = r.id_inventario_maquina
        LEFT JOIN observacion_revision o ON o.id_revision = r.id_revision
        WHERE r.id_estado_revision = 1
        ORDER BY r.fecha_revision DESC
    """)
    revisiones = cursor.fetchall()
    return revisiones

def actualizar_observacion_tecnico(id_revision, observacion_tecnico):
    cursor.execute("""
       UPDATE observacion_revision
        SET observacion_tecnico = %s, fecha = NOW()
        WHERE id_revision = %s
    """, (observacion_tecnico, id_revision))
    connection.commit()

import pymysql.cursors

def datos_usuario(id_usuario, rol=None):
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    if rol:
        cursor.execute('''
            SELECT u.id_usuario, u.identificacion, u.nombre, u.apellido, 
                   u.edad, u.correo, u.telefono, u.contrasena, 
                   g.tipo, u.id_plan_trabajo, u.id_rol, r.nombre AS rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            JOIN genero g ON u.id_genero = g.id_genero
            WHERE u.id_usuario = %s AND r.nombre = %s
        ''', (id_usuario, rol))
    else:
        cursor.execute('''
            SELECT u.id_usuario, u.identificacion, u.nombre, u.apellido, 
                   u.edad, u.correo, u.telefono, u.contrasena, 
                   g.tipo, u.id_plan_trabajo, u.id_rol, r.nombre AS rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            JOIN genero g ON u.id_genero = g.id_genero
            WHERE u.id_usuario = %s
        ''', (id_usuario,))

    usuario = cursor.fetchone()
    cursor.close()
    return usuario


def actualizar_datos_usuario(id_usuario, nombre, apellido, identificacion, edad, correo, telefono, contrasena=None):
    hashed_password = hash_password(contrasena)

    if hashed_password:
        cursor.execute("""
            UPDATE usuario
            SET nombre = %s,
                apellido = %s,
                identificacion = %s,
                edad = %s,
                correo = %s,
                telefono = %s,
                contrasena = %s
            WHERE id_usuario = %s
        """, (nombre, apellido, identificacion, edad, correo, telefono, contrasena_hash, id_usuario))
    else:
        cursor.execute("""
            UPDATE usuario
            SET nombre = %s,
                apellido = %s,
                identificacion = %s,
                edad = %s,
                correo = %s,
                telefono = %s
            WHERE id_usuario = %s
        """, (nombre, apellido, identificacion, edad, correo, telefono, id_usuario))
    connection.commit()
    return True

#CREACION Y ASIGNACION DE LAS RUTINAS
def insertar_rutina(nombre, descripcion, id_plan, id_maquina, dia_semana):
    cursor.execute("""
        INSERT INTO rutina (nombre, descripcion, id_plan_trabajo, id_maquina, dia_semana)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, descripcion, id_plan, id_maquina, dia_semana))
    connection.commit()
    return cursor.lastrowid  # devuelve el id de la nueva rutina


def insertar_zona_cuerpo(nombre_zona, id_rutina):
    cursor.execute("""
        INSERT INTO zona_cuerpo (nombre, id_rutina)
        VALUES (%s, %s)
    """, (nombre_zona, id_rutina))
    connection.commit()


def obtener_rutinas_por_plan(id_plan):
    cursor.execute("""
        SELECT r.nombre, r.descripcion, r.dia_semana, z.nombre AS zona, m.nombre AS maquina
        FROM rutina r
        LEFT JOIN zona_cuerpo z ON r.id_rutina = z.id_rutina
        LEFT JOIN maquina m ON r.id_maquina = m.id_maquina
        WHERE r.id_plan_trabajo = %s
        ORDER BY FIELD(r.dia_semana, 'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
    """, (id_plan,))
    return cursor.fetchall()

def obtener_rutinas_por_plan(id_plan):
    cursor.execute("""
        SELECT r.nombre, r.descripcion, r.dia_semana, 
               z.nombre AS zona, 
               m.nombre AS maquina
        FROM rutina r
        LEFT JOIN zona_cuerpo z ON r.id_rutina = z.id_rutina
        LEFT JOIN maquina m ON r.id_maquina = m.id_maquina
        WHERE r.id_plan_trabajo = %s
        ORDER BY FIELD(r.dia_semana, 
                       'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
    """, (id_plan,))
    return cursor.fetchall()

def obtener_cliente_por_plan(id_plan):
    cursor.execute("""
        SELECT m.id_miembro, m.nombre, m.apellido, u.correo, u.identificacion
        FROM asignacion_pla_trabajo a
        JOIN miembros m ON a.id_miembro_plan = m.id_miembro
        JOIN usuario u ON m.id_usuario = u.id_usuario
        WHERE a.id_plan = %s
    """, (id_plan,))
    return cursor.fetchone()  # Un solo cliente
