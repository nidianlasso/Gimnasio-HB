from flask_mysqldb import MySQL
import pymysql
from functools import wraps
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, make_response
from datetime import datetime, date, timedelta

app = Flask(__name__, static_folder='static', template_folder='template')
# Configura la conexión a la base de datos MySQL
connection = pymysql.connect(host="localhost", user="root", passwd="12345", database="bd_gimnasio2")
cursor = connection.cursor()

def obtenerUsuarios():
    cursor.execute("SELECT * FROM bd_gimnasio2.usuario")
    rows = cursor.fetchall()
    cursor.close()  # Asegúrate de cerrar el cursor
    return rows


# Función para validar el login del usuario
def validarLogin(identificacion, contrasena):
    info_user = check_credentials(identificacion, contrasena)
    
    if info_user:
        # Desempaquetar diccionario
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
            resp = redirect(url_for('profile_coach'))
        elif rol.lower() == "recepcionista":
            resp = redirect(url_for('profile_receptionist'))

        resp.set_cookie('identificacion', str(user_identificacion))
        return resp

    error = "Credenciales incorrectas. Intente de nuevo."
    return render_template('login.html', error=error)



# Función para verificar las credenciales en la base de datos
def check_credentials(identificacion, contrasena):
    cursor.execute("""
        SELECT LOWER(r.nombre) AS rol, u.identificacion, u.id_usuario
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        WHERE u.identificacion = %s AND u.contrasena = %s
    """, (identificacion, contrasena))

    row = cursor.fetchone()
    if row:
        return {
            'rol': row[0],
            'identificacion': row[1],
            'id_usuario': row[2]
        }
    return None




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
            "fecha": str(fila[0]),  # ✅ aquí el cambio
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
        return resultado[0]  # ID de membresía usuario
    return None


#Verificar que no tenga una reserva de la maquina seguida
def consultar_bloques_contiguos(id_membresia_usuario, hora_inicio):
    # Asegurarse de que la hora tenga el formato correcto "HH:MM:SS"
    try:
        hora_actual = datetime.strptime(hora_inicio, "%H:%M:%S")
    except ValueError:
        # Si viene en formato "HH:MM", lo convertimos a "HH:MM:00"
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


#FIN RESERVA DE LAS CLASES