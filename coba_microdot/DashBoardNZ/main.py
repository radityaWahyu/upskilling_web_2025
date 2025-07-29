import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from microdot import Microdot, Response, send_file
import urequests as requests
import random
#import netwo5rk
import time
#import machine

app = Microdot()
Response.default_content_type = 'application/json'

SSID = "BOE-"
PASSWORD = ""	

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
ip_address = '192.168.57.154' #connect_wifi(SSID, PASSWORD)

# API Cuaca (Gantilah API_KEY dengan API dari OpenWeatherMap)
API_KEY = "3f5c97ba51c98cb66a97c7fd54f105fa"
CITY = "Surabaya"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

@app.route('/api/weather')
def get_weather(request):
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()

        # Ambil parameter yang diperlukan
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
        return weather_data

    except Exception as e:
        return {"error": str(e)}, 500

def read_temperature():
    sensor_temp = 45#machine.ADC(4)  # Sensor internal di ADC4
    conversion_factor = 3.3 / 65535
    reading = 100#sensor_temp.read_u16()  # Baca nilai ADC (0-65535)
    voltage = 50#reading * conversion_factor  # Konversi ke Volt
    temperature = 27 - (voltage - 0.706) / 0.001721  # Hitung suhu
    return round(temperature, 2)

@app.route('/sensor/data')
def get_sensor_data(request):
    data = {
        "temp": read_temperature(),  # Suhu asli dari sensor Rasberry Pico
        "humidity": round(random.uniform(40, 90), 1),  # Kelembaban dalam %
        "air_pressure": round(random.uniform(980, 1050), 1),  # Tekanan dalam hPa
        "altitude": round(random.uniform(0, 500), 1),  # Ketinggian dalam meter

        "temp2": read_temperature(),  # Suhu asli dari sensor Rasberry Pico
        "humidity2": round(random.uniform(40, 90), 1),  # Kelembaban dalam %
        "air_pressure2": round(random.uniform(980, 1050), 1),  # Tekanan dalam hPa
        "altitude2": round(random.uniform(0, 500), 1)  # Ketinggian dalam meter
    }
    return data

@app.route('/')
def index(request):
    return send_file('templates/index.html')

@app.route('/static/<path:path>')
def static_files(request, path):
    return send_file('static/' + path)

# Inisialisasi LED di GPIO 2 (bisa ubah pin sesuai kebutuhan)
led = 1#machine.Pin("LED", machine.Pin.OUT)
led_state = False  # Status awal LED

@app.route('/toggle_led')
def toggle_led(request):
    global led_state
    led_state = not led_state  # Toggle status LED
    led.value(led_state)  # Nyalakan/matikan LED

    status = "ON" if led_state else "OFF"
    return {"status": status}

#API Flask
FLASK_API_URL = "http://192.168.57.154:5000/api/bengkel"  # Sesuaikan dengan URL Flask kamu

#TAMPILKAN API dari FLASK
@app.route('/api/inventory')
def get_inventory(request):
    try:
        response = requests.get(FLASK_API_URL)  # Ambil dari Flask
        data = response.json()  # Ubah ke JSON
        print(data)
        response.close()  # Tutup request
        return data  # Kirim ke frontend

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    app.run(host=ip_address, port=5005, debug=True)
