import network
import time
import machine
import onewire
import ds18x20
from umqtt.simple import MQTTClient

# 🔹 Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# 🔹 Configuración del broker MQTT
mqtt_broker = "192.168.228.100"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/sensores"

# 🔹 Configuración del sensor KY-001 (DS18B20)
pin_sensor = machine.Pin(4)  # Cambia según tu conexión
ow = onewire.OneWire(pin_sensor)
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

# 🛜 Función para conectar a Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# 📡 Función para conectar al broker MQTT
def connect_mqtt():
    try:
        client = MQTTClient("sensor_temp_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# 🔄 Función para leer y enviar temperatura por MQTT
def publish_temperature(client):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return
    
    if not roms:
        print("No se encontraron sensores DS18B20")
        return

    try:
        ds.convert_temp()  # Iniciar medición de temperatura
        time.sleep_ms(750)  # Esperar la conversión (750ms recomendados)
        
        for rom in roms:
            temp = ds.read_temp(rom)
            if temp == 85.0 or temp == -127.0:  # Valores erróneos típicos
                print("Error en la lectura del sensor, reintentando...")
            else:
                payload = str(temp)  # Convertir temperatura a string
                client.publish(mqtt_topic, payload)
                print("Temperatura enviada:", temp, "°C")
    
    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)

# 🔥 Main
connect_wifi()
client = connect_mqtt()

while True:
    publish_temperature(client)
    time.sleep(10)  # Enviar cada 10 segundos