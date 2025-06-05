function cargarFormularioEdicionVenta(idVenta) {
    fetch(`/ventas/editar/${idVenta}/`)
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar el formulario de edición.');
            return response.text();
        })
        .then(html => {
            document.getElementById('editarVentaContent').innerHTML = html;
        })
        .catch(error => alert(error));
}

function prepararModalEliminarVenta(idVenta, nombreCliente) {
    document.getElementById('nombreVentaEliminar').textContent = nombreCliente;
    document.getElementById('formEliminarVenta').action = `/ventas/eliminar/${idVenta}/`;
}

// Cargar formulario de agregar venta en el modal
document.querySelector('[data-bs-target="#agregarVentaModal"]').addEventListener('click', () => {
    fetch('/ventas/nueva/')
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar el formulario de venta.');
            return response.text();
        })
        .then(html => {
            document.getElementById('agregarVentaContent').innerHTML = html;
        })
        .catch(error => alert(error));
});

/////////////////////////////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function () {
    inicializarModalVenta('#agregarVentaModal');  // Modal para crear venta
    inicializarModalVenta('#editarVentaModal');   // Modal para editar venta
});

function inicializarModalVenta(modalSelector) {
    const modalVenta = document.querySelector(modalSelector);
    if (!modalVenta) return;

    modalVenta.addEventListener('shown.bs.modal', function () {
        console.log('Modal abierto:', modalSelector);

        const container = modalVenta.querySelector('#productosContainer');
        if (!container) {
            console.warn('No existe productosContainer dentro del modal');
            return;
        }

        const totalForms = modalVenta.querySelector('[id$="TOTAL_FORMS"]');
        const btnAgregarProducto = modalVenta.querySelector('#btnAgregarProducto');

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

                inputPrecioUnitario.value = precioUnitario.toLocaleString('es-ES');
                inputTotal.value = total.toLocaleString('es-ES');

                totalVenta += isNaN(total) ? 0 : total;
            });

            const totalVentaSpan = modalVenta.querySelector('#totalVenta');
            if (totalVentaSpan) {
                totalVentaSpan.textContent = totalVenta.toLocaleString('es-ES');
            }
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
                fila.remove();
                actualizarTotales();
                actualizarTotalForms();
            }
        }

        function actualizarTotalForms() {
            const currentForms = container.querySelectorAll('tr').length;
            totalForms.value = currentForms;
        }

        // Asignar eventos a filas existentes
        container.querySelectorAll('tr').forEach(agregarEventosFila);

        // Evitar duplicados en el botón
        if (btnAgregarProducto) {
            const newBtnAgregarProducto = btnAgregarProducto.cloneNode(true);
            btnAgregarProducto.parentNode.replaceChild(newBtnAgregarProducto, btnAgregarProducto);

            newBtnAgregarProducto.addEventListener('click', function () {
                const currentFormCount = parseInt(totalForms.value);
                const lastRow = container.querySelector('tr:last-child');
                const newRow = lastRow.cloneNode(true);

                newRow.querySelectorAll('input, select').forEach(input => {
                    if (!input.name) return;
                    const regex = /-(\d+)-/;
                    input.name = input.name.replace(regex, `-${currentFormCount}-`);
                    if (input.id) input.id = input.id.replace(regex, `-${currentFormCount}-`);

                    if (input.tagName === 'INPUT') {
                        if (input.type === 'text' || input.type === 'number') {
                            if (input.classList.contains('precio-unitario') || input.classList.contains('total-a-pagar')) {
                                input.value = '0.00';
                            } else {
                                input.value = '';
                            }
                        }
                        if (input.type === 'checkbox') {
                            input.checked = false;
                        }
                    } else if (input.tagName === 'SELECT') {
                        input.selectedIndex = 0;
                    }
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

// Enviar el formulario por AJAX
$(document).on('submit', '#formEditarVenta', function(e) {
    e.preventDefault();
    const form = $(this);
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function(response) {
            if (response.success) {
                $('#editarVentaModal').modal('hide');
                location.reload();
            } else if (response.html) {
                $('#editarVentaModal .modal-content').html(response.html);
            }
        },
        error: function(xhr) {
            $('#editarVentaModal .modal-content').html(xhr.responseText);
        }
    });
});

