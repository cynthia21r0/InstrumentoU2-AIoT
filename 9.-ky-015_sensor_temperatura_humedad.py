import network
import time
import dht
from machine import Pin
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.187.101"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/sensores"

# Configuración del sensor DHT11
dht_pin = Pin(4)  # GPIO donde está conectado el DHT11
sensor_dht = dht.DHT11(dht_pin)

# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("sensor_temp_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos cada 10 segundos
def publish_data(client):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return
    
    try:
        sensor_dht.measure()  # Tomar medición
        temp = sensor_dht.temperature()  # Obtener temperatura en °C

        payload = str(temp)  # Convertir el valor a string
        client.publish(mqtt_topic, payload)
        print("Datos enviados:", payload)

    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)

# Main
connect_wifi()
client = connect_mqtt()

while True:
    publish_data(client)
    time.sleep(10)  # Esperar 10 segundos antes del próximo envío