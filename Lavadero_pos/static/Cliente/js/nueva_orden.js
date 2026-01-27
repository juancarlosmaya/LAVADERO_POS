// Manejador de eventos para Nueva Orden

document.addEventListener('DOMContentLoaded', function() {
    // Agregar event listeners a los checkboxes de servicios al cargar la página
    agregarEventListenersServicios();
});

function agregarEventListenersServicios() {
    const checkboxes = document.querySelectorAll('.service-checkbox');
    
    checkboxes.forEach(checkbox => {
        // Remover listeners anteriores evitando duplicados
        checkbox.removeEventListener('change', calcularTotal);
        checkbox.addEventListener('change', calcularTotal);
    });
}

function calcularTotal() {
    const checkboxes = document.querySelectorAll('.service-checkbox:checked');
    let total = 0;
    
    checkboxes.forEach(checkbox => {
        const precio = parseFloat(checkbox.getAttribute('data-price')) || 0;
        total += precio;
    });
    
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    
    if (subtotalElement) {
        subtotalElement.textContent = `$${total.toFixed(0)}`;
    }
    if (totalElement) {
        totalElement.textContent = `$${total.toFixed(0)}`;
    }
}
