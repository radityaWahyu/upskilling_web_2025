import json
import random
import asyncio
import network
import time
from microdot import Microdot, send_file
from microdot.websocket import with_websocket
from machine import Pin,ADC
from bme_module import BME280Module

# Setup Wi-Fi
SSID = "BOE-"
PASSWORD = ""
#SSID = "free2"
#PASSWORD = "asusa455l"
scl = Pin(22)
sda = Pin(21)
pinLDR = ADC(35)


lamp1 = 0
lamp2 = 0
pump1 = 0
pump2 = 0

pinLamp1 = Pin(13,Pin.OUT)
pinLamp2 = Pin(12,Pin.OUT)
pinPump1 = Pin(14,Pin.OUT)
pinPump2 = Pin(27,Pin.OUT)

pinLamp1.off()
pinLamp2.off()
pinPump1.off()
pinPump2.off()
#pinLDR = ADC(15)

bme_module = BME280Module(0, scl, sda)

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


# Hubungkan ke Wi-Fi
ip_address = connect_wifi(SSID, PASSWORD)
#ip_address = "192.168.56.22"

# # Inisialisasi Microdot
app = Microdot()

# Rute utama untuk halaman web
@app.route('/')
def index(request):
    return send_file('templates/index2.html')


# Rute untuk file CSS dan JavaScript
@app.route('/static/<filename>')
def static_files(request, filename):
    return send_file(f'static/{filename}')

# API untuk mengontrol lampu
@app.route('/api/lamp1', methods=['POST'])
def control_lamp_1(request):
    global lamp1

    status = int(request.json.get('status'))
    lamp1 = status
    
    print("status lampu",status)
    pinLamp1.value(status)

    print("status lampu 1", lamp1)
    response = {
        "status": status
    }

    return response

@app.route('/api/lamp2', methods=['POST'])
def control_lamp_2(request):
    global lamp2

    status = request.json.get('status')
    lamp2 = status
    pinLamp2.value(int(status))

    print("status lampu 2", lamp2)
    response = {
        "status": status
    }

    return response

@app.route('/api/pump1', methods=['POST'])
def control_pump_1(request):
    global pump1

    status = request.json.get('status')
    pump1 = status

    pinPump1.value(int(status))
    
    print("status Pompa 1",pump1)
    response = {
        "status": status
    }

    return response

@app.route('/api/pump2', methods=['POST'])
def control_pump_2(request):
    global pump2

    status = request.json.get('status')
    pump2 = status

    pinPump2.value(int(status))

    print("status pompa 2", pump2)
    response = {
        "status": status
    }

    return response


@app.route('/dashboard')
@with_websocket
async def web_socket_temperature(request, ws):
    global lamp1, lamp2, pump1, pump2

    data = {}

    new_lamp1 = 1
    new_lamp2 = 1
    new_pump1 = 1
    new_pump2 = 1
   
    while True:   
        temp, pressure,humdt, altitude = bme_module.get_sensor_readings()
        # await ws.receive()
        data['temperature'] = round(temp,0)
        data['pressure'] = round(pressure,0)
        data['altitude'] = round(altitude,0)
        
        dataLDR = pinLDR.read_u16()
        light = round((dataLDR/65535)*100,0)
        
        if light == 100:
            statusLight = 0
        else:
            statusLight = 1
            
        
        data['ldr_signal'] = statusLight


        if lamp1 != new_lamp1:
            data['lamp_1'] = lamp1
            new_lamp1 = lamp1
        elif lamp1 == new_lamp1 and 'lamp_1' in data:
            del data['lamp_1']
            
        if lamp2 != new_lamp2:
            data['lamp_2'] = lamp2
            new_lamp2 = lamp2
        elif lamp2 == new_lamp2 and 'lamp_2' in data:
            del data['lamp_2']

        if pump1 != new_pump1:
            data['pump_1'] = pump1
            new_pump1 = pump1
        elif pump1 == new_pump1 and 'pump_1' in data:
            del data['pump_1']
        
        if pump2 != new_pump2:
            data['pump_2'] = pump2
            new_pump2 = pump2
        elif pump2 == new_pump2 and 'pump_2' in data:
            del data['pump_2']

        if len(data) > 0:
            print(data)
            await ws.send(json.dumps(data))
            await asyncio.sleep(1)
   

# Jalankan server
print(ip_address)
                 

try:
    if __name__ == '__main__':
        app.run(host=ip_address, port=5001, debug=True)
except KeyboardInterrupt:
    pass