let printCharacteristic = null;

async function connectAndPrint() {
    const status = document.getElementById('status');
    const btn = event.target;

    try {
        if (!navigator.bluetooth) {
            throw new Error("Bluetooth no soportado en este navegador.");
        }

        status.innerText = "Buscando impresora Bluetooth...";
        const device = await navigator.bluetooth.requestDevice({
            acceptAllDevices: true,
            optionalServices: ['000018f0-0000-1000-8000-00805f9b34fb']
        });

        status.innerText = "Conectando con impresora...";
        const server = await device.gatt.connect();
        const service = await server.getPrimaryService('000018f0-0000-1000-8000-00805f9b34fb');
        printCharacteristic = await service.getCharacteristic('00002af1-0000-1000-8000-00805f9b34fb');

        status.innerText = "Enviando documento...";
        await sendPrintData();
        status.innerText = "✅ Documento enviado a impresora exitosamente.";
        btn.disabled = false;

    } catch (error) {
        console.error(error);
        status.innerText = "❌ Error: " + error.message;
        btn.disabled = false;
    }
}

async function sendPrintData() {
    const encoder = new TextEncoder();

    // Comandos ESC/POS
    const esc = "\x1B";
    const init = esc + "@";
    const center = esc + "a1";
    const left = esc + "a0";
    const boldOn = esc + "E1";
    const boldOff = esc + "E0";

    // Obtener datos del ticket desde el DOM
    const ordenId = document.querySelector('.ticket-numero').textContent.split('#')[1].trim();
    const placa = document.querySelectorAll('.ticket-valor')[2].textContent;
    const tipoVehiculo = document.querySelectorAll('.ticket-valor')[3].textContent;
    const clienteEl = document.querySelectorAll('.ticket-valor')[4];
    const cliente = clienteEl ? clienteEl.textContent : 'Cliente';
    const totalMonto = document.querySelector('.total-monto').textContent;

    let text = init + center + boldOn + "EMOTORS POS\n" + boldOff +
        "Autolavado Profesional\n" +
        "Soacha, Cundinamarca\n" +
        "--------------------------------\n" +
        left +
        "ORDEN: #" + ordenId + "\n" +
        "PLACA: " + placa + "\n" +
        "TIPO: " + tipoVehiculo + "\n" +
        "CLIENTE: " + cliente + "\n" +
        "--------------------------------\n" +
        center + boldOn + "SERVICIOS\n" + boldOff + left;

    // Recopilar servicios del DOM
    document.querySelectorAll('.linea').forEach(linea => {
        const nombre = linea.querySelector('.linea-nombre').textContent;
        const precio = linea.querySelector('.linea-precio').textContent;
        text += nombre + "\n";
        text += "              " + precio + "\n";
    });

    text += "--------------------------------\n" +
        "TOTAL: " + totalMonto + "\n" +
        "--------------------------------\n" +
        center + "¡Gracias por su visita!\n" +
        "Conserva este tiquet\n\n\n\n";

    const data = encoder.encode(text);
    await printCharacteristic.writeValue(data);
}
