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