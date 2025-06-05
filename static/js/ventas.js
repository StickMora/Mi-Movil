function cargarFormularioEdicionVenta(idVenta) {
    // console.log(`DEBUG: Cargando formulario de edición para venta ID ${idVenta}`);
    fetch(`/ventas/editar/${idVenta}/`)
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar el formulario de edición.');
            return response.text();
        })
        .then(html => {
            // console.log("DEBUG: Formulario de edición cargado correctamente");
            document.getElementById('editarVentaContent').innerHTML = html;
            inicializarModalVenta('#editarVentaModal');
        })
        .catch(error => {
            console.error("ERROR:", error);
            alert(error);
        });
}

function prepararModalEliminarVenta(idVenta, nombreCliente) {
    // console.log(`DEBUG: Preparando modal para eliminar venta ID ${idVenta}, cliente: ${nombreCliente}`);
    document.getElementById('nombreVentaEliminar').textContent = nombreCliente;
    document.getElementById('formEliminarVenta').action = `/ventas/eliminar/${idVenta}/`;
}

// Cargar formulario de agregar venta en el modal
document.querySelector('[data-bs-target="#agregarVentaModal"]').addEventListener('click', () => {
    // console.log("DEBUG: Cargando formulario para nueva venta");
    fetch('/ventas/nueva/')
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar el formulario de venta.');
            return response.text();
        })
        .then(html => {
            // console.log("DEBUG: Formulario nueva venta cargado");
            document.getElementById('agregarVentaContent').innerHTML = html;
        })
        .catch(error => {
            console.error("ERROR:", error);
            alert(error);
        });
});

document.addEventListener('DOMContentLoaded', function () {
    // console.log("DEBUG: DOM cargado, inicializando modales");
    inicializarModalVenta('#agregarVentaModal');
    inicializarModalVenta('#editarVentaModal');

    // Enviar el formulario de edición por AJAX 
    document.body.addEventListener('submit', function (e) {
        if (e.target && e.target.id === 'formEditarVenta') {
            e.preventDefault();
            const form = e.target;
            const url = form.action;
            const method = form.method.toUpperCase();
            const formData = new FormData(form);

            // console.log('DEBUG: Enviando formulario de edición...');
            fetch(url, {
                method: method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
            })
            .then(response => response.json())
            .then(data => {
                // console.log('DEBUG: Respuesta recibida:', data);
                if (data.success) {
                    // console.log("DEBUG: Éxito al actualizar venta, ocultando modal y recargando página");
                    const modalElement = document.querySelector('#editarVentaModal');
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    if (modal) modal.hide();
                    location.reload();
                } else if (data.html) {
                    // console.log("DEBUG: Error en formulario, actualizando contenido modal");
                    document.querySelector('#editarVentaModal .modal-content').innerHTML = data.html;
                }
            })
            .catch(error => {
                console.error("ERROR al enviar formulario:", error);
                document.querySelector('#editarVentaModal .modal-content').innerHTML = `<p class="text-danger">Error: ${error}</p>`;
            });
        }
    });
});

function inicializarModalVenta(modalSelector) {
    const modalVenta = document.querySelector(modalSelector);
    if (!modalVenta) {
        console.warn(`WARN: No se encontró modal con selector ${modalSelector}`);
        return;
    }

    modalVenta.addEventListener('shown.bs.modal', function () {
        // console.log(`DEBUG: Modal abierto: ${modalSelector}`);

        const container = modalVenta.querySelector('#productosContainer');
        if (!container) {
            console.warn('WARN: No existe productosContainer dentro del modal');
            return;
        }

        const totalForms = modalVenta.querySelector('[id$="TOTAL_FORMS"]');
        const btnAgregarProducto = modalVenta.querySelector('#btnAgregarProducto');

        function formatearNumeroConComas(numero) {
            const entero = Math.round(numero);
            return entero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }

        function actualizarTotales() {
            let totalVenta = 0;
            const rows = container.querySelectorAll('tr');

            rows.forEach(row => {
                const selectProducto = row.querySelector('.producto-select');
                const inputCantidad = row.querySelector('.cantidad-input');
                const inputPrecioUnitario = row.querySelector('.precio-unitario');
                const inputTotal = row.querySelector('.total-a-pagar');

                if (!selectProducto || !inputCantidad || !inputPrecioUnitario || !inputTotal) return;

                const optionSelected = selectProducto.options[selectProducto.selectedIndex];
                const precioUnitario = parseFloat(optionSelected?.getAttribute('data-precio') || '0') || 0;
                const cantidad = parseInt(inputCantidad.value) || 0;
                const total = precioUnitario * cantidad;

                inputPrecioUnitario.value = formatearNumeroConComas(precioUnitario);
                inputTotal.value = formatearNumeroConComas(total);

                totalVenta += isNaN(total) ? 0 : total;
            });

            const totalVentaSpan = modalVenta.querySelector('#totalVenta');
            if (totalVentaSpan) {
                totalVentaSpan.textContent = formatearNumeroConComas(totalVenta);
            }
            // console.log(`DEBUG: Total de venta actualizado: ${formatearNumeroConComas(totalVenta)}`);
        }

        function agregarEventosFila(row) {
            const selectProducto = row.querySelector('.producto-select');
            const inputCantidad = row.querySelector('.cantidad-input');
            const btnEliminar = row.querySelector('.eliminar-fila');

            if (selectProducto) {
                selectProducto.removeEventListener('change', actualizarTotales);
                selectProducto.addEventListener('change', actualizarTotales);
            }
            if (inputCantidad) {
                inputCantidad.removeEventListener('input', actualizarTotales);
                inputCantidad.addEventListener('input', actualizarTotales);
            }
            if (btnEliminar) {
                btnEliminar.removeEventListener('click', eliminarFila);
                btnEliminar.addEventListener('click', eliminarFila);
            }
        }

        function eliminarFila(event) {
            const fila = event.target.closest('tr');
            if (fila) {
                // console.log("DEBUG: Eliminando fila de producto");
                fila.remove();
                actualizarTotales();
                actualizarTotalForms();
            }
        }

        function actualizarTotalForms() {
            const currentForms = container.querySelectorAll('tr').length;
            totalForms.value = currentForms;
            // console.log(`DEBUG: TOTAL_FORMS actualizado a ${currentForms}`);
        }

        container.querySelectorAll('tr').forEach(agregarEventosFila);

        if (btnAgregarProducto) {
            // Clonar botón para evitar duplicados de eventos
            const newBtnAgregarProducto = btnAgregarProducto.cloneNode(true);
            btnAgregarProducto.parentNode.replaceChild(newBtnAgregarProducto, btnAgregarProducto);

            newBtnAgregarProducto.addEventListener('click', function () {
                // console.log("DEBUG: Botón agregar producto pulsado");
                const currentFormCount = parseInt(totalForms.value);
                const lastRow = container.querySelector('tr:last-child');
                const newRow = lastRow.cloneNode(true);

                newRow.querySelectorAll('input, select').forEach(input => {
                    input.name = input.name.replace(/\d+/, currentFormCount);
                    input.id = input.id.replace(/\d+/, currentFormCount);

                    if (input.type === 'text' || input.type === 'number') input.value = '';
                    if (input.tagName === 'SELECT') input.selectedIndex = 0;
                });

                container.appendChild(newRow);
                totalForms.value = currentFormCount + 1;
                agregarEventosFila(newRow);
                actualizarTotales();
            });
        }

        actualizarTotales();
    });
}
