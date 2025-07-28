#import network
import time
from microdot import Microdot, send_file
import random

# Setup koneksi Wi-Fi
SSID = "BOE-"
PASSWORD = ""
'''
def connect_wifi(ssid, password):
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
ip_address = '192.168.57.78' #connect_wifi(SSID, PASSWORD)

# Inisialisasi Microdot
app = Microdot()

# Rute utama
@app.route('/')
def index(request):
    return send_file('templates/index2.html')

# Rute untuk file CSS
@app.route('/static/<filename>')
def static_files(request, filename):
    return send_file(f'static/{filename}')

# Rute API data suhu dan kelembaban
@app.route('/api/data')
def data_api(request):
    # Data simulasi
    suhu = round(random.uniform(20,35),2)
    humi = round(random.uniform(60,100),2)
    data = {
        "temperature": suhu,
        "humidity": humi,
    }
    return data

# Mulai server
if __name__ == '__main__':
    #print(ip_address)
    app.run(host=ip_address, port=5000, debug=True)

