/*MOSTRAR LA INFORMACION DE LOS USUARIOS*/
function getListUsers() {
    const tablaCuerpo = document.querySelector('#miembrosTabla tbody');
    const tabla = document.getElementById('miembrosTabla');
    tabla.style.display = 'table';

    tablaCuerpo.innerHTML = '';
    fetch('/list-members')
        .then(response => {
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();  // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log(data);
            data.forEach(user => {
                // Crear una fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila
                const celdaId = document.createElement('td');
                celdaId.textContent = user[0];
                fila.appendChild(celdaId);

                const celdaNombre = document.createElement('td');
                celdaNombre.textContent = user[1];
                fila.appendChild(celdaNombre);

                const celdaApellido = document.createElement('td');
                celdaApellido.textContent = user[2];
                fila.appendChild(celdaApellido);

                const celdaEdad = document.createElement('td');
                celdaEdad.textContent = user[3];
                fila.appendChild(celdaEdad);

                const celdaCorreo = document.createElement('td');
                celdaCorreo.textContent = user[4];
                fila.appendChild(celdaCorreo);


                const celdaTelefono = document.createElement('td');
                celdaTelefono.textContent = user[5];
                fila.appendChild(celdaTelefono);

                const celdaRol = document.createElement('td');
                celdaRol.textContent = user[6];
                fila.appendChild(celdaRol);

                // Agregar la fila al cuerpo de la tabla
                tablaCuerpo.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}
/*---MOSTRAR LA INFORMACION DE LOS USUARIOS*/

/*---MOSTRAR LA INFORMACION DE LA BUSQUEDA DE USUARIOS*/
function getSearchUsers() {
    const cuerpoTabla = document.querySelector('#busquedaUsuarios tbody');
    const tabla = document.getElementById('busquedaUsuarios');
    const busqueda = document.getElementById('busqueda_usuario').value;
    tabla.style.display = 'table';
    cuerpoTabla.innerHTML = '';
    fetch('/search-users', {
        method: "POST",
        body: JSON.stringify({ identificacion: busqueda }),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => {
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();  // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Informacion!!!!");

            console.log(data);
            data.forEach(user => {
                // Crear una fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila
                const celdaId = document.createElement('td');
                celdaId.textContent = user[0];
                fila.appendChild(celdaId);

                const celdaNombre = document.createElement('td');
                celdaNombre.textContent = user[1];
                fila.appendChild(celdaNombre);

                const celdaApellido = document.createElement('td');
                celdaApellido.textContent = user[2];
                fila.appendChild(celdaApellido);

                const celdaEdad = document.createElement('td');
                celdaEdad.textContent = user[3];
                fila.appendChild(celdaEdad);

                const celdaCorreo = document.createElement('td');
                celdaCorreo.textContent = user[4];
                fila.appendChild(celdaCorreo);


                const celdaTelefono = document.createElement('td');
                celdaTelefono.textContent = user[5];
                fila.appendChild(celdaTelefono);

                const celdaGenero = document.createElement('td');
                celdaGenero.textContent = user[6];
                fila.appendChild(celdaGenero);

                const celdaPlanTrabajo = document.createElement('td');
                celdaPlanTrabajo.textContent = user[7];
                fila.appendChild(celdaPlanTrabajo);

                const celdaRol = document.createElement('td');
                celdaRol.textContent = user[8];
                fila.appendChild(celdaRol);

                // Agregar la fila al cuerpo de la tabla
                cuerpoTabla.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

/*ASIGNACION DE MEMBRESIAS */
function assign_membreship() {
    const asignacionMembresia = document.getElementById('tablaRegistros').getElementsByTagName('tbody')[0];
    fetch('/assign_membreship')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json(); // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Información recibida:", data);
            // Limpiar la tabla antes de agregar nuevas filas
            asignacionMembresia.innerHTML = '';

            // Filtrar los datos para mostrar solo aquellos con información incompleta
            const datosFiltrados = data.filter(info_user => {
                return !info_user[3] || !info_user[4] || !info_user[5] || !info_user[6]; // costos, tipo, fechaInicio, estadoMembresia
            });

            // Agregar filas a la tabla
            datosFiltrados.forEach(info_user => {
                // Crear una nueva fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila para las 3 primeras columnas
                const id = document.createElement('td');
                id.textContent = info_user[0]; // Identificación
                fila.appendChild(id);

                const nombre = document.createElement('td');
                nombre.textContent = info_user[1]; // Nombre
                fila.appendChild(nombre);

                const apellido = document.createElement('td');
                apellido.textContent = info_user[2]; // Apellido
                fila.appendChild(apellido);

                // Crear la celda para Membresía con un botón
                const membresiaCelda = document.createElement('td');
                const botonMembresia = document.createElement('button');
                botonMembresia.textContent = 'Asignar';
                botonMembresia.className = 'btn btn-primary';

                // Añadir el evento de clic al botón "Asignar"
                botonMembresia.onclick = function () {
                    // Limpia los campos del modal
                    document.getElementById('id_membresia').value = ''; 
                    document.getElementById('fechaInicio').value = ''; 
                    document.getElementById('fechaFin').value = ''; 
                    document.getElementById('estadoMembresia').value = ''; 
                    
                    const usuarioId = info_user[8]; // Asumiendo que info_user[0] es el usuario_id
                    document.getElementById('usuarioId').value = usuarioId; 
                
                    // Abre el modal
                    $('#detallesMembresia').modal('show');
                };
                

                // Agregar el botón a la celda y la celda a la fila
                membresiaCelda.appendChild(botonMembresia);
                fila.appendChild(membresiaCelda);

                // Agregar la fila al cuerpo de la tabla
                asignacionMembresia.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}
function update_membreship(){
    const asignacionMembresia = document.getElementById('actualizacionMembresia').getElementsByTagName('tbody')[0];
    fetch('/assign_membreship')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json(); // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Información recibida:", data);
            // Limpiar la tabla antes de agregar nuevas filas
            asignacionMembresia.innerHTML = '';

            // Filtrar los datos para mostrar solo aquellos con información incompleta
            const datosFiltrados = data.filter(info_user => {
                return info_user[3] || info_user[4] || info_user[5] || info_user[6]; // costos, tipo, fechaInicio, estadoMembresia
            });

            // Agregar filas a la tabla
            datosFiltrados.forEach(info_user => {
                // Crear una nueva fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila para las 3 primeras columnas
                const id = document.createElement('td');
                id.textContent = info_user[0]; // Identificación
                fila.appendChild(id);

                const nombre = document.createElement('td');
                nombre.textContent = info_user[1]; // Nombre
                fila.appendChild(nombre);

                const apellido = document.createElement('td');
                apellido.textContent = info_user[2]; // Apellido
                fila.appendChild(apellido);

                // Crear la celda para Membresía con un botón
                const membresiaCelda = document.createElement('td');
                const botonMembresia = document.createElement('button');
                botonMembresia.textContent = 'Actualizar';
                botonMembresia.className = 'btn btn-primary';

                // Añadir el evento de clic al botón "Asignar"
                botonMembresia.onclick = function () {
                    // Limpia los campos del modal
                    document.getElementById('tipoMembresia').value = ''; 
                    document.getElementById('tipoMembresia').value = info_user[10];
                    console.log(info_user[10]);
                    document.getElementById('fechaInicio').value = ''; 
                    document.getElementById('fechaInicio').value = info_user[5]; 
                    console.log(info_user[5]);
                    document.getElementById('fechaFin').value = '';
                    document.getElementById('fechaFin').value = info_user[6];
                    console.log(info_user[6]);
                    document.getElementById('estadoMembresia').value = '';
                    document.getElementById('estadoMembresia').value = info_user[7]; 
                    console.log("USUARIO QUE LLEGA");
                    console.log(info_user[8]);
                    console.log(info_user[9]);

                    const usuarioId = info_user[8]; 
                    const membresiaUsuario = info_user[9];
                    // Asumiendo que info_user[0] es el usuario_id
                    document.getElementById('id_user_update').value = usuarioId; 
                    document.getElementById('id_membresia_usuario').value = membresiaUsuario;
                    // Abre el modal
                    $('#updateMembresia').modal('show');
                };
                

                // Agregar el botón a la celda y la celda a la fila
                membresiaCelda.appendChild(botonMembresia);
                fila.appendChild(membresiaCelda);

                // Agregar la fila al cuerpo de la tabla
                asignacionMembresia.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

/*GESTION DE LAS MAQUINAS */
function getListMachine() {
    const tablaCuerpo = document.querySelector('#listaMaquinas tbody');
    const tabla = document.getElementById('listaMaquinas');
    tabla.style.display = 'table';

    tablaCuerpo.innerHTML = '';
    fetch('/list-machine')
        .then(response => {
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();  // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log(data);
            data.forEach(user => {
                // Crear una fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila
                const nombreMaquina = document.createElement('td');
                nombreMaquina.textContent = user[0];
                fila.appendChild(nombreMaquina);

                const serialMaquina = document.createElement('td');
                serialMaquina.textContent = user[1];
                fila.appendChild(serialMaquina);

                const fechaCompleta = new Date(user[2]);

                // UTC SIRVE PARA MOSTRAR LA FECHA EXACTA SIN VERSE AFECTADA POR EL SERVIDOR
                const dia = fechaCompleta.getUTCDate();
                const mes = fechaCompleta.getUTCMonth() + 1;
                const anio = fechaCompleta.getUTCFullYear();
                // FORMATO DE LA FECHA
                const fechaFormateada = `${dia}/${mes}/${anio}`;
                const fechaCompra = document.createElement('td');
                fechaCompra.textContent = fechaFormateada;
                fila.appendChild(fechaCompra);

                console.log(fechaCompleta);

                const precioMaquina = document.createElement('td');
                precioMaquina.textContent = user[3];
                fila.appendChild(precioMaquina);

                const proveedorMaquina = document.createElement('td');
                proveedorMaquina.textContent = user[4];
                fila.appendChild(proveedorMaquina);

                const disponibilidadMaquina = document.createElement('td');
                disponibilidadMaquina.textContent = user[5] === 1 ? 'Disponible' : 'No Disponible';
                fila.appendChild(disponibilidadMaquina);

                // Agregar la fila al cuerpo de la tabla
                tablaCuerpo.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

//Disponibilidad de maquinas administrador
$('#maquinasDisponibles').on('show.bs.modal', function () {
    available_machines_page();  // Esta es la función que cargará los datos
});

function available_machines_page(){
    const visualizacionMaquinasDisponibilidad = document.getElementById('visualizacionDisponibilidad').getElementsByTagName('tbody')[0];
    fetch('/available_machines_page')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            visualizacionMaquinasDisponibilidad.innerHTML = '';  // Limpiar tabla antes de insertar nueva data
            data.forEach(user => {
                const fila = document.createElement('tr');

                const fecha = document.createElement('td');
                const horaInicio = document.createElement('td');
                const horaFin = document.createElement('td');
                const nombreUsuario = document.createElement('td');
                const apellidoUsuario = document.createElement('td');
                const nombreMaquina = document.createElement('td');

                const fechaCompleta = new Date(user.fecha);
                const dia = fechaCompleta.getUTCDate();
                const mes = fechaCompleta.getUTCMonth() + 1;
                const anio = fechaCompleta.getUTCFullYear();
                const fechaFormateada = `${dia}/${mes}/${anio}`;
                fecha.textContent = fechaFormateada;
                horaInicio.textContent = user.hora_inicio;
                horaFin.textContent = user.hora_fin;
                nombreUsuario.textContent = user.nombre;
                apellidoUsuario.textContent = user.apellido;
                nombreMaquina.textContent = user.maquina;

                fila.appendChild(fecha);
                fila.appendChild(horaInicio);
                fila.appendChild(horaFin);
                fila.appendChild(nombreUsuario);
                fila.appendChild(apellidoUsuario);
                fila.appendChild(nombreMaquina);

                visualizacionMaquinasDisponibilidad.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}


function getSearchMachine() {
    const cuerpoTabla = document.querySelector('#busquedaMaquinas tbody');
    const tabla = document.getElementById('busquedaMaquinas');
    const busqueda = document.getElementById('busqueda_maquina').value;
    tabla.style.display = 'table';
    cuerpoTabla.innerHTML = '';
    fetch('/search-machine', {
        method: "POST",
        body: JSON.stringify({ identificacion: busqueda }),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => {
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();  // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Informacion!!!!");

            console.log(data);
            data.forEach(user => {
                // Crear una fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila
                const nombre_maquina = document.createElement('td');
                nombre_maquina.textContent = user[0];
                fila.appendChild(nombre_maquina);

                const fechaCompleta = new Date(user[1]);

                // UTC SIRVE PARA MOSTRAR LA FECHA EXACTA SIN VERSE AFECTADA POR EL SERVIDOR
                const dia = fechaCompleta.getUTCDate();
                const mes = fechaCompleta.getUTCMonth() + 1;
                const anio = fechaCompleta.getUTCFullYear();
                const fechaFormateada = `${dia}/${mes}/${anio}`;
                const fecha_compra = document.createElement('td');
                fecha_compra.textContent = fechaFormateada;
                fila.appendChild(fecha_compra);

                const serial = document.createElement('td');
                serial.textContent = user[2];
                fila.appendChild(serial);

                const proveedor = document.createElement('td');
                proveedor.textContent = user[3];
                fila.appendChild(proveedor);

                const precio = document.createElement('td');
                precio.textContent = user[4];
                fila.appendChild(precio);

                // Agregar la fila al cuerpo de la tabla
                cuerpoTabla.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

/*RECEPCIONISTA */
const duracion_defecto = 60; // Duración por defecto en segundos

function segundosAHHMMSS(segundos) {
    if (isNaN(segundos) || segundos < 0) {
        console.error('Duración inválida:', segundos);
        return '00:00:00'; // Valor por defecto si la duración es inválida
    }
    const horas = Math.floor(segundos / 3600);
    const minutos = Math.floor((segundos % 3600) / 60);
    const secs = segundos % 60;

    return `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}
let inicio; // Declaración global
let isActive = false; // Flag para controlar el estado

function registrarIngreso() {
    const cedula = document.getElementById('cedula').value;

    fetch('/registrar-ingreso', {
        method: 'POST',
        body: JSON.stringify({ cedula: cedula }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Error en la solicitud'); });
        }
        return response.json();
    })
    .then(data => {
        console.log('Datos recibidos:', data);
        const resultadoIngreso = document.getElementById('resultadoIngreso');
        resultadoIngreso.innerHTML = ''; // Limpieza del div

        // Mostrar la información del usuario
        const infoUsuario = document.createElement('div');
        infoUsuario.innerHTML = `
            <p>Nombre: ${data.nombre}</p>
            <p>Apellido: ${data.apellido}</p>
            <p>Rol: ${data.rol}</p>
            <button id="activarBtn">Activar</button>
        `;
        resultadoIngreso.appendChild(infoUsuario);

        // Obtener el estado actual del acceso
        fetch(`/obtener-acceso?id_usuario=${data.id_usuario}`, {
            method: 'GET',
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    console.log('No se encontró acceso, creando uno nuevo...');
                    return crearAcceso(data.id_usuario);
                }
                throw new Error('Error al obtener el estado de acceso');
            }
            return response.json();
        })
        .then(accesoData => {
            // Si accesoData es undefined, crear un nuevo acceso y devolver el tipo de acceso
            const boton = document.getElementById('activarBtn');
            boton.textContent = accesoData.tipo_acceso === 'Active' ? 'Desactivar' : 'Activar';
            isActive = accesoData.tipo_acceso === 'Active'; // Actualiza el estado

            // Manejo del clic del botón
            boton.addEventListener('click', () => {
                const nuevoTipoAcceso = boton.textContent === 'Desactivar' ? 'Inactive' : 'Active';

                if (nuevoTipoAcceso === 'Active') {
                    // Activar acceso
                    inicio = new Date(); // Establece el tiempo de inicio
                    console.log('Inicio establecido:', inicio); // Verifica el valor de inicio
                    const fecha = inicio.toISOString(); // Fecha actual
                    const duracionFormato = segundosAHHMMSS(duracion_defecto); // Usar la duración por defecto

                    fetch('/guardar-acceso', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ fecha, duracion: duracionFormato, tipo_acceso: nuevoTipoAcceso, id_usuario: data.id_usuario })
                    })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        }
                        throw new Error('Error en la solicitud');
                    })
                    .then(data => {
                        console.log('Acceso registrado:', data);
                        boton.textContent = 'Desactivar'; // Cambia el texto del botón
                        isActive = true; // Marca que está activo
                    })
                    .catch(error => {
                        console.error('Error al guardar el acceso:', error);
                    });
                } else {
                    // Desactivar acceso
                    if (!isActive) {
                        console.error('No se puede desactivar, el acceso no está activo');
                        return;
                    }

                    const fin = new Date();
                    const duracionSegundos = Math.floor((fin - inicio) / 1000); // Duración en segundos
                    console.log('Duración en segundos:', duracionSegundos);

                    if (duracionSegundos < 0) {
                        console.error('Duración inválida, el tiempo de inicio es posterior al tiempo de fin');
                        return; // Evita continuar si la duración es inválida
                    }

                    const duracionFormato = segundosAHHMMSS(duracionSegundos); // Convertir a formato HH:MM:SS

                    fetch('/guardar-acceso', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ fecha: fin.toISOString(), duracion: duracionFormato, tipo_acceso: nuevoTipoAcceso, id_usuario: data.id_usuario })
                    })
                    .then(response => {
                        if (response.ok) {
                            return response.json();
                        }
                        throw new Error('Error en la solicitud');
                    })
                    .then(data => {
                        console.log('Acceso desactivado:', data);
                        boton.textContent = 'Activar'; // Cambia el texto del botón
                        isActive = false; // Marca que ya no está activo
                    })
                    .catch(error => {
                        console.error('Error al desactivar el acceso:', error);
                    });
                }
            });
        })
        .catch(error => {
            console.error('Error al obtener el estado de acceso:', error);
            resultadoIngreso.innerHTML = `<p style="color:red;">${error.message}</p>`;
        });
    })
    .catch(error => {
        console.error('Hubo un problema con la solicitud:', error);
        const resultadoIngreso = document.getElementById('resultadoIngreso');
        resultadoIngreso.innerHTML = `<p style="color:red;">${error.message}</p>`;
    });
}

// Función para crear un acceso nuevo si no existe
function crearAcceso(id_usuario) {
    const fecha = new Date().toISOString();
    const duracionFormato = segundosAHHMMSS(duracion_defecto); // Usar la duración por defecto
    const tipo_acceso = 'Active'; // Tipo de acceso inicial

    return fetch('/guardar-acceso', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fecha, duracion: duracionFormato, tipo_acceso, id_usuario })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al crear acceso');
        }
        return response.json();
    })
    .then(data => {
        console.log('Nuevo acceso creado:', data);
        return { tipo_acceso }; // Devuelve el tipo de acceso que se acaba de crear
    })
    .catch(error => {
        console.error('Error al crear el acceso:', error);
    });
}

//FUNCION PARA ASIGNAR ENTRENADOR A MIEMBRO
function assign_coach() {
    const asignacionEntrenador = document.querySelector('#tablaAsignacionEntrenador tbody');
    fetch('/assign-coach')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json(); // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Información recibida:", data);

            // Filtrar los datos para obtener solo miembros y entrenadores activos
            const miembrosActivos = data.filter(info_user => 
                info_user[4] === 'Active' && info_user[6] === 'Miembro' // info_user[4] es el tipo de acceso y info_user[6] es el rol
            );
            const entrenadoresActivos = data.filter(info_user => 
                info_user[4] === 'Active' && info_user[6] === 'Entrenador' 
            );

            // Limpiar la tabla antes de agregar nuevas filas
            asignacionEntrenador.innerHTML = ''; 

            // Agregar filas a la tabla
            miembrosActivos.forEach(info_user => {
                // Crear una nueva fila
                const fila = document.createElement('tr');

                const id = document.createElement('td');
                id.textContent = info_user[0]; // Identificación
                fila.appendChild(id);

                const nombre = document.createElement('td');
                nombre.textContent = info_user[1]; // Nombre
                fila.appendChild(nombre);

                const apellido = document.createElement('td');
                apellido.textContent = info_user[2]; // Apellido
                fila.appendChild(apellido);

                // Validacion del plan de trabajo de instructores y miembros
                const planTrabajoMiembro = info_user[8]; // Plan de trabajo del miembro
                const entrenadorAsignado = entrenadoresActivos.find(entrenador => entrenador[8] === planTrabajoMiembro); // Buscar entrenador con el mismo plan de trabajo

                if (entrenadorAsignado) {
                    // celda del entrenador
                    const entrenadorCelda = document.createElement('td');
                    entrenadorCelda.textContent = entrenadorAsignado[1]; // Nombre del entrenador
                    fila.appendChild(entrenadorCelda);
                } else {
                    // Disponibilidad del entrenador
                    const entrenadorCelda = document.createElement('td');
                    entrenadorCelda.textContent = "Sin entrenador disponible";
                    fila.appendChild(entrenadorCelda);
                }

                // Agregar la fila al cuerpo de la tabla
                asignacionEntrenador.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

function assign_membreship() {
    const asignacionMembresia = document.getElementById('reserva_maquinas').getElementsByTagName('tbody')[0];
    fetch('/assign_membreship')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json(); // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Información recibida:", data);
            // Limpiar la tabla antes de agregar nuevas filas
            asignacionMembresia.innerHTML = '';

            // Filtrar los datos para mostrar solo aquellos con información incompleta
            const datosFiltrados = data.filter(info_user => {
                return !info_user[3] || !info_user[4] || !info_user[5] || !info_user[6]; // costos, tipo, fechaInicio, estadoMembresia
            });

            // Agregar filas a la tabla
            datosFiltrados.forEach(info_user => {
                // Crear una nueva fila
                const fila = document.createElement('tr');

                // Crear y agregar celdas a la fila para las 3 primeras columnas
                const id = document.createElement('td');
                id.textContent = info_user[0]; // Identificación
                fila.appendChild(id);

                const nombre = document.createElement('td');
                nombre.textContent = info_user[1]; // Nombre
                fila.appendChild(nombre);

                const apellido = document.createElement('td');
                apellido.textContent = info_user[2]; // Apellido
                fila.appendChild(apellido);

                // Crear la celda para Membresía con un botón
                const membresiaCelda = document.createElement('td');
                const botonMembresia = document.createElement('button');
                botonMembresia.textContent = 'Asignar';
                botonMembresia.className = 'btn btn-primary';

                // Añadir el evento de clic al botón "Asignar"
                botonMembresia.onclick = function () {
                    // Limpia los campos del modal
                    document.getElementById('id_membresia').value = ''; 
                    document.getElementById('fechaInicio').value = ''; 
                    document.getElementById('fechaFin').value = ''; 
                    document.getElementById('estadoMembresia').value = ''; 
                    
                    const usuarioId = info_user[8]; // Asumiendo que info_user[0] es el usuario_id
                    document.getElementById('usuarioId').value = usuarioId; 
                
                    // Abre el modal
                    $('#detallesMembresia').modal('show');
                };
                

                // Agregar el botón a la celda y la celda a la fila
                membresiaCelda.appendChild(botonMembresia);
                fila.appendChild(membresiaCelda);

                // Agregar la fila al cuerpo de la tabla
                asignacionMembresia.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

