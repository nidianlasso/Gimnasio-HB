let isActive = false;
let inicio = null;



/*MOSTRAR LA INFORMACION DE LOS USUARIOS*/
function getListUsers() {
    const tablaCuerpo = document.querySelector('#miembrosTabla tbody');
    const tabla = document.getElementById('miembrosTabla');
    tabla.style.display = 'table';

    tablaCuerpo.innerHTML = '';
    fetch('/list-members')
        .then(response => {
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();
        })
        .then(data => {
            console.log(data);
            data.forEach(user => {

                const fila = document.createElement('tr');

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
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();
        })
        .then(data => {
            console.log("Informacion!!!!");

            console.log(data);
            data.forEach(user => {
                const fila = document.createElement('tr');

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
            return response.json();
        })
        .then(data => {
            console.log("Información recibida:", data);
            asignacionMembresia.innerHTML = '';

            const datosFiltrados = data.filter(info_user => {
                return !info_user[3] || !info_user[4] || !info_user[5] || !info_user[6]; // costos, tipo, fechaInicio, estadoMembresia
            });


            datosFiltrados.forEach(info_user => {

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


                const membresiaCelda = document.createElement('td');
                const botonMembresia = document.createElement('button');
                botonMembresia.textContent = 'Asignar';
                botonMembresia.className = 'btn btn-primary';


                botonMembresia.onclick = function () {

                    document.getElementById('id_membresia').value = '';
                    document.getElementById('fechaInicio').value = '';
                    document.getElementById('fechaFin').value = '';
                    document.getElementById('estadoMembresia').value = '';

                    const usuarioId = info_user[8];
                    document.getElementById('usuarioId').value = usuarioId;


                    $('#detallesMembresia').modal('show');
                };

                membresiaCelda.appendChild(botonMembresia);
                fila.appendChild(membresiaCelda);


                asignacionMembresia.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}
function update_membreship() {
    const asignacionMembresia = document.getElementById('actualizacionMembresia').getElementsByTagName('tbody')[0];
    fetch('/assign_membreship')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            console.log("Información recibida:", data);
            asignacionMembresia.innerHTML = '';

            // Filtrar los datos para mostrar solo aquellos con información incompleta
            const datosFiltrados = data.filter(info_user => {
                return info_user[3] || info_user[4] || info_user[5] || info_user[6]; // costos, tipo, fechaInicio, estadoMembresia
            });


            datosFiltrados.forEach(info_user => {

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

                const membresiaCelda = document.createElement('td');
                const botonMembresia = document.createElement('button');
                botonMembresia.textContent = 'Actualizar';
                botonMembresia.className = 'btn btn-primary';

                botonMembresia.onclick = function () {
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
                    document.getElementById('id_user_update').value = usuarioId;
                    document.getElementById('id_membresia_usuario').value = membresiaUsuario;
                    $('#updateMembresia').modal('show');
                };
                membresiaCelda.appendChild(botonMembresia);
                fila.appendChild(membresiaCelda);

                asignacionMembresia.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

function abrirModalRevision(idInventario) {
    const modalRevision = document.getElementById("modalRevision");
    const observacionInput = document.getElementById("observacionInput");
    document.getElementById("idMaquinaRevision").value = idInventario;

    observacionInput.value = ""; 
    modalRevision.style.display = "block"; 
}


function initModalRevision() {
    const btnCancelar = document.getElementById("btnCancelarRevision");

    if (btnCancelar) {
        btnCancelar.addEventListener("click", function () {
            $('#modalRevision').modal('hide'); 
        });
    }
}


function getListMachine() {
    const tablaCuerpo = document.querySelector('#listaMaquinas tbody');
    const tabla = document.getElementById('listaMaquinas');
    tabla.style.display = 'table';

    tablaCuerpo.innerHTML = '';
    fetch('/list-machine')
        .then(response => {
            if (!response.ok) { throw new Error('Error en la solicitud'); }
            return response.json();
        })
        .then(data => {
            console.log(data);
            data.forEach(user => {
                const fila = document.createElement('tr');
                const nombreMaquina = document.createElement('td');
                nombreMaquina.textContent = user[0];
                fila.appendChild(nombreMaquina);

                const serialMaquina = document.createElement('td');
                serialMaquina.textContent = user[1];
                fila.appendChild(serialMaquina);

                const fechaCompleta = new Date(user[2]);
                const dia = fechaCompleta.getUTCDate();
                const mes = fechaCompleta.getUTCMonth() + 1;
                const anio = fechaCompleta.getUTCFullYear();
                const fechaFormateada = `${dia}/${mes}/${anio}`;
                const fechaCompra = document.createElement('td');
                fechaCompra.textContent = fechaFormateada;
                fila.appendChild(fechaCompra);

                const precioMaquina = document.createElement('td');
                precioMaquina.textContent = user[3];
                fila.appendChild(precioMaquina);

                const proveedorMaquina = document.createElement('td');
                proveedorMaquina.textContent = user[4];
                fila.appendChild(proveedorMaquina);

                const disponibilidadMaquina = document.createElement('td');
                disponibilidadMaquina.textContent = user[5] === 1 ? 'Disponible' : 'No Disponible';
                fila.appendChild(disponibilidadMaquina);

                const columnaBoton = document.createElement('td');
                if (user[5] !== 1) {
                    const btnRevision = document.createElement('button');
                    btnRevision.textContent = 'Enviar a revisión';
                    btnRevision.classList.add('btn', 'btn-warning', 'btn-sm');
                    btnRevision.dataset.idInventario = user[6]; 

                    if (user[7] === 1) {
                        btnRevision.textContent = 'En revisión';
                        btnRevision.disabled = true; 
                        btnRevision.classList.remove('btn-warning');
                        btnRevision.classList.add('btn-secondary');
                    } else {
                        btnRevision.addEventListener('click', function () {
                            abrirModalRevision(this.dataset.idInventario);
                        });
                    }

                    columnaBoton.appendChild(btnRevision);
                } else {
                    columnaBoton.textContent = '-';
                }
                fila.appendChild(columnaBoton);

                tablaCuerpo.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}


function abrirModalRevision(idInventario) {
    document.getElementById("idMaquinaRevision").value = idInventario;
    $('#modalRevision').modal('show');
}



function enviarRevision(event) {
    event.preventDefault(); // Evita que el formulario se recargue

    const idInventario = document.getElementById("idMaquinaRevision").value;
    const estado = document.getElementById("estadoRevision").value;
    const observacion = document.getElementById("observacionRevision").value;

    if (!idInventario) {
        console.error("No se encontró idInventario");
        return;
    }

    fetch('/enviar-revision', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id_inventario: idInventario,
            estado: estado,
            observacion: observacion
        })
    })
        .then(res => res.json())
        .then(data => {
            console.log("Respuesta:", data);
            alert(data.mensaje || "Revisión enviada");
            const btn = document.querySelector(`button[data-id-inventario="${idInventario}"]`);
            if (btn) {
                btn.textContent = 'En revisión';
                btn.disabled = true;                          
                btn.classList.remove('btn-warning');
                btn.classList.add('btn-secondary');   
            }
            $('#modalRevision').modal('hide'); 
            getListMachine();
        })
        .catch(error => console.error("Error al enviar revisión:", error));
}

function mostrarInformes() {
  document.getElementById("informes").style.display = "block";

  
  let tabla = document.getElementById("tabla-informes");
  tabla.innerHTML = "";

  informes.forEach(informe => {
    let fila = `
      <tr>
        <td>${informe.maquina}</td>
        <td>${informe.fecha}</td>
        <td>
          <span style="padding:4px 8px; border-radius:6px; 
            ${informe.estado === "Pendiente" ? "background:#ffc107; color:#000;" : 
              informe.estado === "En revisión" ? "background:#17a2b8; color:#fff;" : 
              "background:#28a745; color:#fff;"}">
            ${informe.estado}
          </span>
        </td>
        <td>${informe.obs}</td>
        <td>
          <button style="padding:6px 10px; background:#007bff; color:#fff; border:none; border-radius:6px; cursor:pointer;">
            Ver Detalle
          </button>
        </td>
      </tr>
    `;
    tabla.innerHTML += fila;
  });
}



$('#maquinasDisponibles').on('show.bs.modal', function () {
    available_machines_page();
});

function cargarMaquinas(tipo) {
    fetch(`/maquinas?tipo=${tipo}`)
        .then(res => {
            if (!res.ok) throw new Error('No se pudo cargar');
            return res.json();
        })
        .then(data => {
            const tbody = document.getElementById('tablaMaquinas');
            const thead = document.getElementById('tablaEncabezado');
            const tabla = document.getElementById('tablaPrincipal');
            const calendarioContainer = document.getElementById('contenedorCalendario');

            if (tbody) tbody.innerHTML = '';
            if (thead) thead.innerHTML = '';
            if (calendarioContainer) calendarioContainer.innerHTML = '';

            if (tipo === 'disponibilidad_horaria') {
                if (tabla) tabla.style.display = 'none';
                if (calendarioContainer) calendarioContainer.style.display = 'block';
            } else {
                if (tabla) tabla.style.display = 'table';
                if (calendarioContainer) calendarioContainer.style.display = 'none';
            }

            if (tipo === 'reservadas') {
                thead.innerHTML = `
                    <tr>
                        <th>Máquina</th>
                        <th>Nombre</th>
                        <th>Apellido</th>
                        <th>Fecha</th>
                        <th>Inicio</th>
                        <th>Fin</th>
                        <th>Disponibilidad</th>
                    </tr>`;
                data.forEach(item => {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${item.nombre_maquina}</td>
                        <td>${item.nombre}</td>
                        <td>${item.apellido}</td>
                        <td>${formatearFecha(item.fecha)}</td>
                        <td>${item.hora_inicio}</td>
                        <td>${item.hora_fin}</td>
                        <td>${item.disponibilidad}</td>`;
                    tbody.appendChild(fila);
                });
            }

            else if (tipo === 'disponibles') {
                thead.innerHTML = `
                    <tr>
                        <th>Máquina</th>
                        <th>Disponibilidad</th>
                    </tr>`;
                data.forEach(item => {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td>${item.nombre_maquina}</td>
                        <td>${item.disponibilidad}</td>`;
                    tbody.appendChild(fila);
                });
            }

            else if (tipo === 'disponibilidad_horaria') {
                data.forEach(maquina => {
                    const fila = document.createElement('div');
                    fila.className = 'maquina-grid';

                    const nombre = document.createElement('div');
                    nombre.className = 'nombre-maquina';
                    nombre.textContent = maquina.nombre_maquina;
                    fila.appendChild(nombre);

                    const bloques = Object.values(maquina.bloques).flat();

                    bloques.forEach(b => {
                        const bloque = document.createElement('div');
                        bloque.className = `bloque ${b.estado}`;
                        bloque.title = `${b.hora} - ${sumar15(b.hora)}`;

                        if (b.estado === 'disponible') {
                            bloque.style.cursor = 'pointer';

                            bloque.addEventListener('click', () => {
                                console.log('Click detectado en:', maquina.id_maquina, b.hora);
                                reservarBloque(maquina.id_maquina, b.hora);
                            });
                        }

                        fila.appendChild(bloque);
                    });

                    calendarioContainer.appendChild(fila);
                });

            }
        })
        .catch(err => {
            console.error('Error:', err);
        });
}

function reservarBloque(id_maquina, hora_inicio) {
    console.log('Reservando máquina:', id_maquina, 'a las', hora_inicio);

    fetch('/reservar-bloque', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id_maquina: id_maquina,
            hora: hora_inicio
        })
    })

        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                cargarMaquinas('disponibilidad_horaria');
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(err => {
            console.error('Error en la solicitud:', err);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('maquina');

    fetch('/api/maquinas_disponibles')
        .then(res => res.json())
        .then(data => {
            data.forEach(maquina => {
                const opt = document.createElement('option');
                opt.value = maquina.id;
                opt.textContent = maquina.nombre;
                select.appendChild(opt);
            });
        });

    document.getElementById('formReservaMaquina').addEventListener('submit', e => {
        e.preventDefault();

        const data = {
            id_inventario_maquina: select.value,
            hora_inicio: document.getElementById('hora_inicio').value,
            hora_fin: document.getElementById('hora_fin').value
        };

        fetch('/reservar_maquina', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(res => {
                document.getElementById('mensaje').textContent = res.mensaje || res.error;
            });
    });
});

//*******************************************************/

// Utilidad para sumar 15 minutos
function sumar15(horaStr) {
    const [h, m] = horaStr.split(':').map(Number);
    const fecha = new Date();
    fecha.setHours(h, m + 15);
    return fecha.toTimeString().slice(0, 5);
}

function formatearFecha(fechaStr) {
    const [anio, mes, dia] = fechaStr.split('-');
    return `${dia}/${mes}/${anio}`;
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
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json(); 
        })
        .then(data => {
            console.log("Informacion!!!!");

            console.log(data);
            data.forEach(user => {
                const fila = document.createElement('tr');

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
                cuerpoTabla.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

/*RECEPCIONISTA */

function registrarIngreso() {
    const cedula = document.getElementById('cedula').value;

    fetch('/registrar-ingreso', {
        method: 'POST',
        body: JSON.stringify({ cedula }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { 
                throw new Error(err.error || 'Error en la solicitud'); 
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Datos recibidos:', data);
        mostrarUsuario(data);  // 👉 Llamamos a otra función para renderizar
        obtenerAcceso(data.id_usuario); // 👉 Llamamos a la función que consulta acceso
    })
    .catch(error => {
        console.error('Error al registrar ingreso:', error);
    });
}

// 🔹 Mostrar datos del usuario en pantalla
function mostrarUsuario(data) {
    const resultadoIngreso = document.getElementById('resultadoIngreso');
    resultadoIngreso.innerHTML = '';

    const infoUsuario = document.createElement('div');
    infoUsuario.innerHTML = `
        <p>Nombre: ${data.nombre}</p>
        <p>Apellido: ${data.apellido}</p>
        <p>Rol: ${data.rol}</p>
        <button id="activarBtn">Activar</button>
    `;
    resultadoIngreso.appendChild(infoUsuario);
}
// 🔹 Obtener estado de acceso y asignar evento al botón
function obtenerAcceso(id_usuario) {
    fetch(`/obtener-acceso?id_usuario=${id_usuario}`)
        .then(r => {
            if (!r.ok) throw new Error('Error al obtener el estado de acceso');
            return r.json();
        })
        .then(accesoData => {
            let isActive = accesoData.tipo_acceso === 'Active';
            const boton = document.getElementById('activarBtn');
            boton.textContent = isActive ? 'Desactivar' : 'Activar';

            boton.addEventListener('click', () => {
                if (!isActive) {
                    activarAcceso(id_usuario, boton, () => isActive = true);
                } else {
                    desactivarAcceso(id_usuario, boton, () => isActive = false);
                }
            });
        })
        .catch(error => {
            console.error('Error al obtener el estado de acceso:', error);
        });
}
// 🔹 Activar acceso
function activarAcceso(id_usuario, boton, callback) {
    const inicio = new Date();
    fetch('/guardar-acceso', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tipo_acceso: 'Active',
            id_usuario: id_usuario,
            fecha: inicio.toISOString(),
            duracion: "00:00:00"
        })
    })
    .then(r => r.json())
    .then(res => {
        console.log(res);
        boton.textContent = 'Desactivar';
        callback();
    })
    .catch(error => console.error('Error al activar acceso:', error));
}

// 🔹 Desactivar acceso
function desactivarAcceso(id_usuario, boton, callback) {
    fetch('/cambiar-estado-acceso', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_usuario })
    })
    .then(r => r.json())
    .then(res => {
        console.log(res);
        boton.textContent = 'Activar';
        callback();
    })
    .catch(error => console.error('Error al desactivar acceso:', error));
}

//FUNCION PARA ASIGNAR ENTRENADOR A MIEMBRO
function assign_coach() {
    const asignacionEntrenador = document.querySelector('#tablaAsignacionEntrenador tbody');
    fetch('/assign-coach')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json(); 
        })
        .then(data => {
            const miembrosActivos = data.filter(info_user =>
                info_user[4] === 'Active' && info_user[6] === 'Miembro' // info_user[4] es el tipo de acceso y info_user[6] es el rol
            );
            const entrenadoresActivos = data.filter(info_user =>
                info_user[4] === 'Active' && info_user[6] === 'Entrenador'
            );
            asignacionEntrenador.innerHTML = '';

            miembrosActivos.forEach(info_user => {
                const fila = document.createElement('tr');

                const id = document.createElement('td');
                id.textContent = info_user[0];
                fila.appendChild(id);

                const nombre = document.createElement('td');
                nombre.textContent = info_user[1];
                fila.appendChild(nombre);

                const apellido = document.createElement('td');
                apellido.textContent = info_user[2];
                fila.appendChild(apellido);

                const planTrabajoMiembro = info_user[8];
                const entrenadorAsignado = entrenadoresActivos.find(entrenador => entrenador[8] === planTrabajoMiembro);
                if (entrenadorAsignado) {
                    const entrenadorCelda = document.createElement('td');
                    entrenadorCelda.textContent = entrenadorAsignado[1]; 
                    fila.appendChild(entrenadorCelda);
                } else {
                    const entrenadorCelda = document.createElement('td');
                    entrenadorCelda.textContent = "Sin entrenador disponible";
                    fila.appendChild(entrenadorCelda);
                }
                asignacionEntrenador.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

function assign_membreship() {
    const asignacionMembresia = document.getElementById('tablaRegistros').getElementsByTagName('tbody')[0];

    fetch('/assign_membership')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            asignacionMembresia.innerHTML = '';

            const datosFiltrados = data; // Mostrar todos

            datosFiltrados.forEach(info_user => {
                const fila = document.createElement('tr');

                const id = document.createElement('td');
                id.textContent = info_user[0]; // identificacion
                fila.appendChild(id);

                const nombre = document.createElement('td');
                nombre.textContent = info_user[1];
                fila.appendChild(nombre);

                const apellido = document.createElement('td');
                apellido.textContent = info_user[2];
                fila.appendChild(apellido);

                const membresiaCelda = document.createElement('td');
                const botonMembresia = document.createElement('button');
                botonMembresia.textContent = 'Asignar';
                botonMembresia.className = 'btn btn-primary';

                botonMembresia.onclick = function () {
                    document.getElementById('id_membresia').value = '';
                    document.getElementById('fechaInicio').value = '';
                    document.getElementById('fechaFin').value = '';
                    document.getElementById('estadoMembresia').value = '';

                    const usuarioId = info_user[3]; // CORRECTO: índice 3
                    document.getElementById('usuarioId').value = usuarioId;

                    $('#detallesMembresia').modal('show');
                };

                membresiaCelda.appendChild(botonMembresia);
                fila.appendChild(membresiaCelda);
                asignacionMembresia.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

//FUNCION PARA HACER LA RESERVA DE LA MAQUINA
function realizarReserva(data) {
    fetch('/reservar_maquina', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(respuesta => {
            if (respuesta.error) {
                alert("Error: " + respuesta.error);
            } else {
                alert(respuesta.mensaje);
                cargarMaquinas('disponibilidad_horaria');
            }
        })
        .catch(err => {
            console.error('Error al reservar:', err);
            alert('Hubo un error al hacer la reserva.');
        });
}

function cargarDatosEmpleado() {
    const select = document.getElementById("identificacion");
    const nombre = document.getElementById("nombre");
    const apellido = document.getElementById("apellido");
    const salarioInput = document.getElementById("salario");

    const selected = select.options[select.selectedIndex];
    const nombreVal = selected.getAttribute("data-nombre");
    const apellidoVal = selected.getAttribute("data-apellido");
    const salarioVal = parseFloat(selected.getAttribute("data-salario"));

    nombre.value = nombreVal || '';
    apellido.value = apellidoVal || '';
    salarioInput.value = salarioVal.toFixed(2);

    calcularNomina();
}

function calcularNomina() {
    const salario = parseFloat(document.getElementById("salario").value) || 0;
    const auxilio = salario * 0.05;
    const salud = salario * 0.04;
    const pension = salario * 0.04;
    const total_devengado = salario + auxilio;
    const total_deducciones = salud + pension;
    const liquido = total_devengado - total_deducciones;

    document.getElementById("auxilio").value = auxilio.toFixed(2);
    document.getElementById("salud").value = salud.toFixed(2);
    document.getElementById("pension").value = pension.toFixed(2);
    document.getElementById("total_devengado").value = total_devengado.toFixed(2);
    document.getElementById("total_deducciones").value = total_deducciones.toFixed(2);
    document.getElementById("liquido").value = liquido.toFixed(2);
}

