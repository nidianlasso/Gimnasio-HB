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
    fetch('/get_assigned_memberships')
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
                    document.getElementById('tipoMembresia').value = info_user[3]; // id_membresia
                    document.getElementById('fechaInicio').value = info_user[4];
                    document.getElementById('fechaFin').value = info_user[5];
                    document.getElementById('estadoMembresia').value = info_user[6];

                    document.getElementById('id_user_update').value = info_user[0]; // id usuario
                    document.getElementById('id_membresia_usuario').value = info_user[7]; // id membresia_usuario

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

function eliminarMaquina(idInventario) {
    return fetch('/delete-maquina', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ id_inventario: idInventario })
    })
    .then(response => {
        if (!response.ok) throw new Error('Error en la solicitud');
        return response.json();
    });
}

function manejarEliminacion(idInventario) {
    fetch('/delete-maquina', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ id_inventario: idInventario })
    })
    .then(response => {
        if (!response.ok) throw new Error('Error en la solicitud');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Máquina eliminada con éxito');
            getListMachine(); // Refrescar lista
        } else {
            alert('Error al eliminar: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar la máquina');
    });
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
            data.forEach(user => {
                const fila = document.createElement('tr');

                // Nombre
                const nombre = document.createElement('td');
                nombre.textContent = user[0];
                fila.appendChild(nombre);

                // Serial
                const serial = document.createElement('td');
                serial.textContent = user[1];
                fila.appendChild(serial);

                // Fecha de compra formateada
                const fechaCompra = document.createElement('td');
                const fecha = new Date(user[2]);
                const dia = fecha.getUTCDate().toString().padStart(2, '0');
                const mes = (fecha.getUTCMonth() + 1).toString().padStart(2, '0');
                const anio = fecha.getUTCFullYear();
                fechaCompra.textContent = `${dia}/${mes}/${anio}`;
                fila.appendChild(fechaCompra);

                // Precio
                const precio = document.createElement('td');
                precio.textContent = user[3];
                fila.appendChild(precio);

                // Proveedor (nombre visible)
                const proveedor = document.createElement('td');
                proveedor.textContent = user[4];
                fila.appendChild(proveedor);

                // Disponibilidad
                const disponibilidad = document.createElement('td');
                disponibilidad.textContent = user[5] === 1 ? 'Disponible' : 'No Disponible';
                fila.appendChild(disponibilidad);

                // Botón "Enviar a revisión"
                const columnaRevision = document.createElement('td');
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
                    columnaRevision.appendChild(btnRevision);
                } else {
                    columnaRevision.textContent = '-';
                }
                fila.appendChild(columnaRevision);

                // Botón Editar
                const columnaEditar = document.createElement('td');
                const btnEditar = document.createElement('button');
                btnEditar.textContent = 'Editar';
                btnEditar.classList.add('btn', 'btn-primary', 'btn-sm');

                btnEditar.dataset.idInventario = user[6];
                btnEditar.dataset.nombre = user[0];
                btnEditar.dataset.serial = user[1];
                btnEditar.dataset.fechaCompra = user[2];
                btnEditar.dataset.precio = user[3];
                btnEditar.dataset.proveedor = user[7]; // id_proveedor
                btnEditar.dataset.disponibilidad = user[5];

                btnEditar.addEventListener('click', function () {
                    const modalEl = document.getElementById('modalEditarMaquina');
                    if (!modalEl) {
                        console.error('Modal no encontrado');
                        return;
                    }

                    document.getElementById('editarIdInventario').value = this.dataset.idInventario;
                    document.getElementById('editarNombre').value = this.dataset.nombre;
                    document.getElementById('editarSerial').value = this.dataset.serial;

                    const fechaCompleta = new Date(this.dataset.fechaCompra);
                    const yyyy = fechaCompleta.getFullYear();
                    const mm = String(fechaCompleta.getMonth() + 1).padStart(2, '0');
                    const dd = String(fechaCompleta.getDate()).padStart(2, '0');
                    document.getElementById('editarFechaCompra').value = `${yyyy}-${mm}-${dd}`;

                    document.getElementById('editarPrecio').value = this.dataset.precio;

                    const proveedorSelect = document.getElementById('editarProveedor');
                    if (proveedorSelect) proveedorSelect.value = this.dataset.proveedor;

                    document.getElementById('editarDisponibilidad').value = this.dataset.disponibilidad;

                    const modal = new bootstrap.Modal(modalEl);
                    modal.show();
                });

                columnaEditar.appendChild(btnEditar);
                fila.appendChild(columnaEditar);

                // Botón Eliminar
                const columnaEliminar = document.createElement('td');
                const btnEliminar = document.createElement('button');
                btnEliminar.textContent = '❌';
                btnEliminar.classList.add('btn',  'btn-sm');
                btnEliminar.dataset.idInventario = user[6];

                btnEliminar.addEventListener('click', () => {
                    if (confirm('¿Estás seguro de que quieres eliminar esta máquina?')) {
                        manejarEliminacion(btnEliminar.dataset.idInventario);
                    }
                });

                columnaEliminar.appendChild(btnEliminar);
                fila.appendChild(columnaEliminar);

                tablaCuerpo.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}

// Listener para guardar cambios en el modal editar
document.getElementById('btnGuardarCambios').addEventListener('click', function() {
    const form = document.getElementById('formEditarMaquina');
    const formData = new FormData(form);

    fetch('/update-maquina', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) throw new Error('Error al actualizar');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Máquina actualizada con éxito');

            // Cerrar modal usando jQuery de Bootstrap 4
            $('#modalEditarMaquina').modal('hide');

            // Refrescar la lista de máquinas
            getListMachine();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(err => {
        console.error(err);
        alert('Error al actualizar la máquina');
    });
});






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

                        if (b.estado === 'reservado') {
                            bloque.style.cursor = 'pointer';
                            bloque.title += ' (Haz clic para cancelar)';
                            bloque.addEventListener('click', () => {
                                if (confirm("¿Deseas cancelar esta reserva?")) {
                                    fetch('/cancelar-reserva-maquina', {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify({ id_maquina: maquina.id_maquina, hora: b.hora })
                                    })
                                        .then(res => res.json())
                                        .then(data => {
                                            alert(data.message);
                                            if (data.success) {
                                                cargarMaquinas('disponibilidad_horaria'); // recarga la vista para reflejar cambios
                                            }
                                        })
                                        .catch(err => {
                                            alert('Error al cancelar la reserva');
                                            console.error(err);
                                        });
                                }
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
    const form = document.getElementById('formReservaMaquina');

    // Si el formulario y el select existen en esta página
    if (form && select) {
        // Llenar el select con máquinas disponibles
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

        // Escuchar el envío del formulario
        form.addEventListener('submit', e => {
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
    }
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
      return response.json().then(err => { throw new Error(err.error || 'Error en la solicitud'); });
    }
    return response.json();
  })
  .then(data => {
    mostrarUsuario(data);
    obtenerAcceso(data.id_usuario);
    cargarAccesosActivos();  // 🚀 Carga usuarios con acceso activo al mostrar usuario
  })
  .catch(error => {
    console.error('Error al registrar ingreso:', error);
    document.getElementById('resultadoIngreso').innerHTML = `<p class="text-danger">${error.message}</p>`;
  });
}

function cargarAccesosActivos() {
  fetch('/accesos-activos')
    .then(res => {
      if (!res.ok) throw new Error('Error al cargar accesos activos');
      return res.json();
    })
    .then(datos => {
      const tbody = document.querySelector('#tablaAccesosActivos tbody');
      tbody.innerHTML = ''; // limpiar tabla

      datos.forEach(usuario => {
        // usuario = {id_usuario, nombre, apellido, rol}
        const tr = document.createElement('tr');

        tr.innerHTML = `
          <td>${usuario.id_usuario}</td>
          <td>${usuario.nombre}</td>
          <td>${usuario.apellido}</td>
          <td>${usuario.rol}</td>
          <td><button class="btn btn-danger btn-sm" onclick="desactivarAcceso(${usuario.id_usuario}, null, () => cargarAccesosActivos())">Desactivar</button></td>
        `;

        tbody.appendChild(tr);
      });
    })
    .catch(error => {
      console.error('Error al cargar accesos activos:', error);
    });
}
function mostrarUsuario(data) {
  const resultadoIngreso = document.getElementById('resultadoIngreso');
  resultadoIngreso.innerHTML = `
    <p><strong>Nombre:</strong> ${data.nombre}</p>
    <p><strong>Apellido:</strong> ${data.apellido}</p>
    <p><strong>Rol:</strong> ${data.rol}</p>
    <button id="activarBtn" class="btn btn-primary"></button>
  `;
}

function obtenerAcceso(id_usuario) {
  fetch(`/obtener-acceso?id_usuario=${id_usuario}`)
    .then(res => {
      if (!res.ok) throw new Error('Error al obtener el estado de acceso');
      return res.json();
    })
    .then(accesoData => {
      const boton = document.getElementById('activarBtn');
      let isActive = accesoData.tipo_acceso === 'Active';

      boton.textContent = isActive ? 'Desactivar' : 'Activar';
      boton.classList.toggle('btn-danger', isActive);
      boton.classList.toggle('btn-success', !isActive);

      boton.onclick = () => {
        if (isActive) {
          desactivarAcceso(id_usuario, boton, () => {
            isActive = false;
            boton.textContent = 'Activar';
            boton.classList.replace('btn-danger', 'btn-success');
          });
        } else {
          activarAcceso(id_usuario, boton, () => {
            isActive = true;
            boton.textContent = 'Desactivar';
            boton.classList.replace('btn-success', 'btn-danger');
          });
        }
      };
    })
    .catch(error => {
      console.error('Error al obtener el estado de acceso:', error);
      document.getElementById('resultadoIngreso').innerHTML += `<p class="text-danger">${error.message}</p>`;
    });
}

function activarAcceso(id_usuario, boton, callback) {
  const inicio = new Date();
  fetch('/guardar-acceso', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tipo_acceso: 'Active',
      id_usuario,
      fecha: inicio.toISOString(),
      duracion: "00:00:00"
    })
  })
  .then(res => {
    if (!res.ok) throw new Error('Error al activar acceso');
    return res.json();
  })
  .then(() => {
    callback();
  })
  .catch(error => {
    console.error('Error al activar acceso:', error);
    alert('No se pudo activar el acceso');
  });
}

function desactivarAcceso(id_usuario, boton, callback) {
  fetch('/cambiar-estado-acceso', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id_usuario })
  })
  .then(res => {
    if (!res.ok) throw new Error('Error al desactivar acceso');
    return res.json();
  })
  .then(() => {
    callback();
  })
  .catch(error => {
    console.error('Error al desactivar acceso:', error);
    alert('No se pudo desactivar el acceso');
  });
}

// Esperar a que el DOM esté listo y se abra el modal
document.addEventListener('DOMContentLoaded', () => {
  $('#searchUser').on('shown.bs.modal', function () {
    cargarAccesosActivos();
  });
});


//FUNCION PARA ASIGNAR ENTRENADOR A MIEMBRO
function assign_coach() {
    const asignacionEntrenador = document.querySelector('#asignacionEntrenador tbody');

    fetch('/assign-coach')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            // Asumimos que el backend envía:
            // data.miembros y data.entrenadores
            // Cada elemento: [id_usuario, nombre, apellido, tipo_acceso, rol, id_plan_trabajo]

            const miembrosActivos = data.miembros;
            const entrenadoresActivos = data.entrenadores;

            asignacionEntrenador.innerHTML = ''; // Limpiar tabla

            miembrosActivos.forEach(miembro => {
                const fila = document.createElement('tr');

                // ID del miembro
                const id = document.createElement('td');
                id.textContent = miembro[0];
                fila.appendChild(id);

                // Nombre
                const nombre = document.createElement('td');
                nombre.textContent = miembro[1];
                fila.appendChild(nombre);

                // Apellido
                const apellido = document.createElement('td');
                apellido.textContent = miembro[2];
                fila.appendChild(apellido);

                // Dropdown de entrenadores disponibles, filtrando por plan de trabajo
                const tdSelect = document.createElement('td');
                const selectEntrenador = document.createElement('select');
                selectEntrenador.classList.add('form-control');
                selectEntrenador.name = `entrenador_para_${miembro[0]}`;

                // Filtrar entrenadores con el mismo id_plan_trabajo
                const entrenadoresCompatibles = entrenadoresActivos.filter(entrenador => entrenador[5] === miembro[5]);

                if (entrenadoresCompatibles.length === 0) {
                    const option = document.createElement('option');
                    option.text = 'No hay entrenadores compatibles';
                    option.disabled = true;
                    selectEntrenador.appendChild(option);
                } else {
                    entrenadoresCompatibles.forEach(entrenador => {
                        const option = document.createElement('option');
                        option.value = entrenador[0]; // id_entrenador
                        option.text = `${entrenador[1]} ${entrenador[2]}`;
                        selectEntrenador.appendChild(option);
                    });
                }

                tdSelect.appendChild(selectEntrenador);
                fila.appendChild(tdSelect);

                asignacionEntrenador.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}


function guardarCambios() {
    const asignaciones = [];

    // Recolectar asignaciones de los selects
    document.querySelectorAll('select[name^="entrenador_para_"]').forEach(select => {
        const id_miembro = select.name.replace('entrenador_para_', '');
        const id_entrenador = select.value;

        asignaciones.push({
            id_miembro: parseInt(id_miembro),
            id_entrenador: parseInt(id_entrenador)
        });
    });

    console.log('Asignaciones a guardar:', asignaciones); // Verifica en consola

    fetch('/save-assignments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // <-- importante
        },
        body: JSON.stringify(asignaciones)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
        alert('Asignaciones guardadas correctamente.');
    })
    .catch(error => {
        console.error('Error al guardar:', error);
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

//CARGAR LOS CLIENTES ASIGNADOS AL ENTRENADOR
function cargarClientesAsignados(id_entrenador) {
  fetch('/clientes-entrenador-asignado', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id_entrenador })
  })
  .then(response => {
    if (!response.ok) throw new Error('Error al obtener clientes asignados');
    return response.json();
  })
  .then(clientes => {
    const tbody = document.querySelector('#tablaClientesAsignados tbody');
    tbody.innerHTML = '';

    if (clientes.length === 0) {
      document.getElementById('mensaje').style.display = 'block';
      return;
    } else {
      document.getElementById('mensaje').style.display = 'none';
    }

    clientes.forEach(c => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${c.id_usuario}</td>
        <td>${c.nombre}</td>
        <td>${c.apellido}</td>
        <td>
          ${c.tieneRutina ? `
            <div class="btn-group">
              <button type="button" class="btn btn-warning btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                Gestionar Rutina
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/actualizar-rutina/${c.id_usuario}">Actualizar</a></li>
                <li><a class="dropdown-item text-danger" href="#" onclick="eliminarRutina(${c.id_usuario})">Eliminar</a></li>
              </ul>
            </div>
          ` : `
            <a href="/crear-rutina/${c.id_usuario}" class="btn btn-primary btn-sm">Crear Rutina</a>
          `}
        </td>
      `;
      tbody.appendChild(tr);
    });
  })
  .catch(error => {
    console.error(error);
    alert('No se pudieron cargar los clientes asignados.');
  });
}

function eliminarRutina(id_usuario) {
  if (!confirm('¿Seguro que quieres eliminar la rutina? Esta acción no se puede deshacer.')) return;

  fetch(`/eliminar-rutina/${id_usuario}`, {
    method: 'DELETE',
  })
  .then(response => {
    if (!response.ok) throw new Error('Error al eliminar la rutina');
    alert('Rutina eliminada correctamente.');
    // Recarga la lista o actualiza la fila
    cargarClientesAsignados(id_entrenador);
  })
  .catch(error => {
    console.error(error);
    alert('No se pudo eliminar la rutina.');
  });
}



// static/js/asignarRutina.js

function asignarRutina(formId) {
  const form = document.getElementById(formId);

  if (!form) {
    console.error(`No se encontró el formulario con ID '${formId}'`);
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = {};

    // Recorremos todos los valores (incluidos repetidos)
    formData.forEach((value, key) => {
      if (key.endsWith("[]")) {
        // Si es un array (rutinas[1][], rutinas[2][], etc.)
        const cleanKey = key.replace("[]", "");
        if (!data[cleanKey]) {
          data[cleanKey] = [];
        }
        data[cleanKey].push(value);
      } else {
        // Campos normales
        data[key] = value;
      }
    });

    fetch("/asignar-rutina", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (response.ok) {
        alert("✅ Rutina asignada con éxito");
        window.location.href = "/mis-clientes";
      } else {
        alert("❌ Error al asignar la rutina");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("❌ Ocurrió un error");
    });
  });
}
document.addEventListener("DOMContentLoaded", () => {
  asignarRutina("formAsignarRutina");
});
