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

/*GESTION DE LAS MAQUINAS */
// =========================
// Inicialización del modal
// =========================
// =========================
// Función global que abre el modal
// =========================
// =========================
// Función global para abrir el modal
// =========================
function abrirModalRevision(idInventario) {
    const modalRevision = document.getElementById("modalRevision");
    const observacionInput = document.getElementById("observacionInput");

    // Guardamos el ID seleccionado en un input hidden (o data-atributo)
    document.getElementById("idMaquinaRevision").value = idInventario;

    observacionInput.value = ""; // limpiar campo
    modalRevision.style.display = "block"; // mostrar modal
}

// =========================
// Inicializar modal (botón cancelar)
// =================// =========================
// Inicialización del modal de revisión
// =========================
function initModalRevision() {
    // Ya no necesitas document.getElementById ni tocar style.display
    // Bootstrap se encarga de mostrar/ocultar
    const btnCancelar = document.getElementById("btnCancelarRevision");

    if (btnCancelar) {
        btnCancelar.addEventListener("click", function () {
            $('#modalRevision').modal('hide'); // 👈 Ocultar modal con Bootstrap
        });
    }
}


// =========================
// Listado de máquinas
// =========================
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

                // user[0] = nombre, user[1] = serial, etc.
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

                // Columna de disponibilidad
                const disponibilidadMaquina = document.createElement('td');
                disponibilidadMaquina.textContent = user[5] === 1 ? 'Disponible' : 'No Disponible';
                fila.appendChild(disponibilidadMaquina);

                // Columna del botón
                const columnaBoton = document.createElement('td');
                if (user[5] !== 1) {
                    const btnRevision = document.createElement('button');
                    btnRevision.textContent = 'Enviar a revisión';
                    btnRevision.classList.add('btn', 'btn-warning', 'btn-sm');
                    btnRevision.dataset.idInventario = user[6];  // <-- Guardar ID

                    // 👉 Si ya fue enviada, se deshabilita
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


// =========================
// Abrir modal y setear datos
// =========================
// Función para abrir modal de revisión
// =========================
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
                btn.disabled = true;                          // que no haga nada
                btn.classList.remove('btn-warning');
                btn.classList.add('btn-secondary');          // cambia color
            }
            $('#modalRevision').modal('hide'); // cerrar modal
            getListMachine();
        })
        .catch(error => console.error("Error al enviar revisión:", error));
}

function mostrarInformes() {
  document.getElementById("informes").style.display = "block";

  // Ejemplo de datos simulados (esto luego vendrá de tu BD Flask/MySQL)
  const informes = [
    { maquina: "Bicicleta Estática", fecha: "2025-08-20", estado: "En revisión", obs: "Cadena floja" },
    { maquina: "Caminadora", fecha: "2025-08-21", estado: "Reparada", obs: "Motor reemplazado" },
    { maquina: "Press de banca", fecha: "2025-08-23", estado: "Pendiente", obs: "A la espera de repuestos" }
  ];

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


//Disponibilidad de maquinas administrador
$('#maquinasDisponibles').on('show.bs.modal', function () {
    available_machines_page();  // Esta es la función que cargará los datos DESDE BACK
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

            // Limpia solo si existen
            if (tbody) tbody.innerHTML = '';
            if (thead) thead.innerHTML = '';
            if (calendarioContainer) calendarioContainer.innerHTML = '';

            // Mostrar u ocultar contenedores según el tipo
            if (tipo === 'disponibilidad_horaria') {
                if (tabla) tabla.style.display = 'none';
                if (calendarioContainer) calendarioContainer.style.display = 'block';
            } else {
                if (tabla) tabla.style.display = 'table';
                if (calendarioContainer) calendarioContainer.style.display = 'none';
            }

            // Tabla: máquinas reservadas
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

            // Tabla: máquinas disponibles
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

            // Calendario: disponibilidad horaria
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

//***************************************************** */
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

    // Cargar máquinas disponibles
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

    // Enviar reserva
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
            if (!response.ok) { throw new Error('Error en la solicitud'); } return response.json();  // Parsear la respuesta a JSON
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
const duracion_defecto = 60;

function segundosAHHMMSS(segundos) {
    if (isNaN(segundos) || segundos < 0) {
        console.error('Duración inválida:', segundos);
        return '00:00:00';
    }
    const horas = Math.floor(segundos / 3600);
    const minutos = Math.floor((segundos % 3600) / 60);
    const secs = segundos % 60;

    return `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}
let inicio;
let isActive = false;

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
            resultadoIngreso.innerHTML = '';

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
                                return;
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

                const planTrabajoMiembro = info_user[8]; // Plan de trabajo del miembro
                const entrenadorAsignado = entrenadoresActivos.find(entrenador => entrenador[8] === planTrabajoMiembro);
                if (entrenadorAsignado) {
                    const entrenadorCelda = document.createElement('td');
                    entrenadorCelda.textContent = entrenadorAsignado[1]; // Nombre del entrenador
                    fila.appendChild(entrenadorCelda);
                } else {
                    // Disponibilidad del entrenador
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
    const asignacionMembresia = document.getElementById('reserva_maquinas').getElementsByTagName('tbody')[0];
    fetch('/assign_membreship')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            asignacionMembresia.innerHTML = '';

            // Filtrar los datos para mostrar solo aquellos con información incompleta
            const datosFiltrados = data.filter(info_user => {
                return !info_user[3] || !info_user[4] || !info_user[5] || !info_user[6]; // costos, tipo, fechaInicio, estadoMembresia
            });
            datosFiltrados.forEach(info_user => {
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

                    // Abre el modal
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
                cargarMaquinas('disponibilidad_horaria'); // Recarga EL calendario CUANDO SE RESERVA
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

