function filterServices() {
    const type = document.getElementById('id_tipo').value;
    const items = document.querySelectorAll('.servicio-item');
    items.forEach(item => {
        if (item.dataset.category === type) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
            item.querySelector('input').checked = false;
        }
    });
    calcularTotal();
}

function calcularTotal() {
    const checked = Array.from(document.querySelectorAll('.servicio-checkbox:checked'));
    const total = checked.reduce((sum, el) => {
        const precio = parseFloat(el.closest('.servicio-item').querySelector('.servicio-precio').textContent.replace('$', ''));
        return sum + precio;
    }, 0);
    document.getElementById('subtotal').textContent = total.toFixed(0);
    document.getElementById('total').textContent = total.toFixed(0);
}

document.addEventListener('DOMContentLoaded', function() {
    const tipoSelect = document.getElementById('id_tipo');
    if (tipoSelect) {
        tipoSelect.addEventListener('change', filterServices);
        filterServices();
    }

    document.querySelectorAll('.servicio-checkbox').forEach(el => {
        el.addEventListener('change', calcularTotal);
    });

    document.getElementById('orderForm').onsubmit = (e) => {
        const selectedServices = Array.from(document.querySelectorAll('input[name="servicios"]:checked')).map(cb => cb.value);

        if (selectedServices.length === 0) {
            e.preventDefault();
            alert("Debes seleccionar al menos un servicio.");
            return false;
        }
        
        return true;
    };
});

