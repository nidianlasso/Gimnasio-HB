/*MOSTRAR LA INFORMACION DE LOS USUARIOS*/
function getListUsers() {
    const tablaCuerpo = document.querySelector('#miembrosTabla tbody');
    const tabla = document.getElementById('miembrosTabla');
    tabla.style.display = 'table';

    tablaCuerpo.innerHTML = '';
    fetch('/list-members')
        .then(response => {if (!response.ok) {throw new Error('Error en la solicitud');}return response.json();  // Parsear la respuesta a JSON
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
function getSearchUsers(){
    const cuerpoTabla = document.querySelector('#busquedaUsuarios tbody');
    const tabla = document.getElementById('busquedaUsuarios');
    const busqueda = document.getElementById('busqueda_usuario').value;
    tabla.style.display = 'table';
    cuerpoTabla.innerHTML = '';
    fetch('/search-users', {
        method: "POST",
        body: JSON.stringify({nombre:busqueda}),
        headers: {
            'Content-Type': 'application/json'
        },
      })
    .then(response => {if (!response.ok) {throw new Error('Error en la solicitud');}return response.json();  // Parsear la respuesta a JSON
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
function assign_membreship(){
    const tablaAsignacion = document.querySelector('#membresiaAsignacion tbody');
    const tablaMembresia = document.getElementById('busquedaUsuarios');
    fetch('/assig-membreship')
    .then(response => {if (!response.ok) {throw new Error('Error en la solicitud');}return response.json();  // Parsear la respuesta a JSON
        })
        .then(data => {
            console.log("Informacion!!!!");
            
            console.log(data); 
            data.forEach(user => {
            // Crear una fila
            console.log("dentro de la funcion")

            // Agregar la fila al cuerpo de la tabla
            cuerpoTabla.appendChild(fila);
        });
        })
        .catch(error => {
            console.error('Hubo un problema con la solicitud:', error);
        });
}