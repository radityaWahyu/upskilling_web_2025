// Update status lampu di halaman
async function updateLampStatus() {
    try {
        const response = await fetch('/api/lamp/status');
        const data = await response.json();
        document.getElementById('lamp-status').innerText = data.status === 'on' ? 'Menyala' : 'Mati';
    } catch (error) {
        console.error('Error fetching lamp status:', error);
    }
}

// Hidupkan lampu
async function turnOnLamp() {
    try {
        await fetch('/api/lamp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'on' })
        });
        updateLampStatus();
    } catch (error) {
        console.error('Error turning on the lamp:', error);
    }
}

// Matikan lampu
async function turnOffLamp() {
    try {
        await fetch('/api/lamp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'off' })
        });
        updateLampStatus();
    } catch (error) {
        console.error('Error turning off the lamp:', error);
    }
}

// Tambahkan event listener ke tombol
document.getElementById('lamp-on').addEventListener('click', turnOnLamp);
document.getElementById('lamp-off').addEventListener('click', turnOffLamp);

// Perbarui status lampu saat halaman dimuat
updateLampStatus();
