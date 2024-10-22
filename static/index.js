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
// function registrarIngreso() {
//     const cedula = document.getElementById('cedula').value;

//     fetch('/registrar-ingreso', {
//         method: 'POST',
//         body: JSON.stringify({ cedula: cedula }),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//     .then(response => {
//         if (!response.ok) {
//             return response.json().then(err => { throw new Error(err.error || 'Error en la solicitud'); });
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Datos recibidos:', data);
//         const resultadoIngreso = document.getElementById('resultadoIngreso');
//         resultadoIngreso.innerHTML = ''; // Limpieza del div

//         // Mostrar la información del usuario
//         const infoUsuario = document.createElement('div');
//         infoUsuario.innerHTML = `
//             <p>Nombre: ${data.nombre}</p>
//             <p>Apellido: ${data.apellido}</p>
//             <p>Rol: ${data.rol}</p>
//             <button id="activarBtn">Activar</button>
//         `;
//         resultadoIngreso.appendChild(infoUsuario);

//         // Obtener el estado actual del acceso
//         fetch(`/obtener-acceso?id_usuario=${data.id_usuario}`, {
//             method: 'GET',
//         })
//         .then(response => {
//             if (!response.ok) {
//                 // Si hay un error al obtener el acceso, asumimos que no existe y lo creamos
//                 if (response.status === 404) {
//                     console.log('No se encontró acceso, creando uno nuevo...');
//                     return crearAcceso(data.id_usuario);
//                 }
//                 throw new Error('Error al obtener el estado de acceso');
//             }
//             return response.json();
//         })
//         .then(accesoData => {
//             console.log('Tipo de ID de usuario:', typeof accesoData.id_usuario);
            
//             const boton = document.getElementById('activarBtn');
//             // Cambiar el texto del botón según el estado
//             boton.textContent = accesoData.tipo_acceso === 'Active' ? 'Desactivar' : 'Activar';

//             // Manejo del clic del botón
//             boton.addEventListener('click', () => {
//                 const fecha = new Date().toISOString(); // Fecha actual
//                 const duracion = 60; // Duración
//                 const nuevoTipoAcceso = boton.textContent === 'Desactivar' ? 'Inactive' : 'Active';

//                 // Cambiar el texto del botón
//                 boton.textContent = nuevoTipoAcceso === 'Inactive' ? 'Activar' : 'Desactivar';

//                 fetch('/guardar-acceso', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     },
//                     body: JSON.stringify({ fecha, duracion, tipo_acceso: nuevoTipoAcceso, id_usuario: data.id_usuario })
//                 })
//                 .then(response => {
//                     if (response.ok) {
//                         return response.json();
//                     }
//                     throw new Error('Error en la solicitud');
//                 })
//                 .then(data => {
//                     console.log('Acceso registrado:', data);
//                 })
//                 .catch(error => {
//                     console.error('Error al guardar el acceso:', error);
//                 });
//             });
//         })
//         .catch(error => {
//             console.error('Error al obtener el estado de acceso:', error);
//             resultadoIngreso.innerHTML = `<p style="color:red;">${error.message}</p>`;
//         });
//     })
//     .catch(error => {
//         console.error('Hubo un problema con la solicitud:', error);
//         const resultadoIngreso = document.getElementById('resultadoIngreso');
//         resultadoIngreso.innerHTML = `<p style="color:red;">${error.message}</p>`;
//     });
// }

// const inicio = new Date(); // Fecha y hora actual

// // Función para crear un acceso nuevo si no existe
// function crearAcceso(id_usuario) {
//     const fin = new Date();
    
//     const fecha = new Date().toISOString();
//     const duracion = 60; // Duración por defecto
//     const tipo_acceso = 'Active'; // Tipo de acceso inicial

//     return fetch('/guardar-acceso', {  //guardar los datos
//         method: 'POST',
//         headers: {
//            'Content-Type': 'application/json'
//         },
//        body: JSON.stringify({ fecha, duracion, tipo_acceso, id_usuario: data.id_usuario })
//         })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Error al crear acceso');
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Nuevo acceso creado:', data);
//     })
//     .catch(error => {
//         console.error('Error al crear el acceso:', error);
//     });
// }
// // Función para cambiar el estado a Inactive
// function desactivarAcceso(id_usuario) {
//     fetch('/cambiar-estado-acceso', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ id_usuario }),
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Error en la respuesta de la red');
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Acceso desactivado:', data);
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }

const DURACION_DEFAULT = 60; // Duración por defecto en segundos
let inicio; // Variable para guardar la hora de inicio

// Función para convertir segundos a formato HH:MM:SS
function segundosAHHMMSS(segundos) {
    const horas = Math.floor(segundos / 3600);
    const minutos = Math.floor((segundos % 3600) / 60);
    const secs = segundos % 60;

    return `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

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
            const boton = document.getElementById('activarBtn');
            boton.textContent = accesoData.tipo_acceso === 'Active' ? 'Desactivar' : 'Activar';

            // Manejo del clic del botón
            boton.addEventListener('click', () => {
                const nuevoTipoAcceso = boton.textContent === 'Desactivar' ? 'Inactive' : 'Active';

                boton.textContent = nuevoTipoAcceso === 'Inactive' ? 'Activar' : 'Desactivar';

                if (nuevoTipoAcceso === 'Active') {
                    // Al activar, guardar la hora de inicio
                    inicio = new Date(); 
                    const fecha = inicio.toISOString(); // Fecha actual
                    const duracionFormato = segundosAHHMMSS(DURACION_DEFAULT); // Usar la duración por defecto

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
                    })
                    .catch(error => {
                        console.error('Error al guardar el acceso:', error);
                    });
                } else {
                    // Al desactivar, calcular la duración
                    const fin = new Date();
                    const duracionSegundos = Math.floor((fin - inicio) / 1000); // Duración en segundos

                    // Verifica que la duración sea válida
                    if (isNaN(duracionSegundos) || duracionSegundos < 0) {
                        console.error('Duración inválida:', duracionSegundos);
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
    const duracionFormato = segundosAHHMMSS(DURACION_DEFAULT); // Usar la duración por defecto
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
    })
    .catch(error => {
        console.error('Error al crear el acceso:', error);
    });
}
