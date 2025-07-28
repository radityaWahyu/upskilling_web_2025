#import network
import time
from microdot import Microdot, send_file
#from machine import Pin

# Setup Wi-Fi
SSID = "Nama_Jaringan_WiFi"
PASSWORD = "Password_WiFi"


'''def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Menghubungkan ke Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Masih mencoba...")

    print("Wi-Fi Terhubung!")
    print("Alamat IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]
'''

# Hubungkan ke Wi-Fi
ip_address = '192.168.57.78'#connect_wifi(SSID, PASSWORD)

# Inisialisasi Microdot
app = Microdot()

# Setup GPIO untuk lampu (LED)
led = 15#Pin("LED", Pin.OUT)
led_state = {"status": "off"}  # State lampu (on/off)


# Rute utama untuk halaman web
@app.route('/')
def index(request):
    return send_file('templates/index.html')


# Rute untuk file CSS dan JavaScript
@app.route('/static/<filename>')
def static_files(request, filename):
    return send_file(f'static/{filename}')


# API untuk mengontrol lampu
@app.route('/api/lamp', methods=['POST'])
def control_lamp(request):
    global led_state
    action = request.json.get('action')
    if action == "on":
        #led.on()
        led_state["status"] = "on"
    elif action == "off":
        #led.off()
        led_state["status"] = "off"
    return led_state


# API untuk mendapatkan status lampu
@app.route('/api/lamp/status')
def lamp_status(request):
    return led_state


# Jalankan server
#print(ip_address)
#app.run(host=ip_address, port=5001)
if __name__ == '__main__':
    app.run(host=ip_address, port=5001, debug=True)