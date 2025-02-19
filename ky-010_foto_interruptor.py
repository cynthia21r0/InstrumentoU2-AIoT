import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.187.100"  # Nueva IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/sensores"  # Nuevo tema

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

# Configuración del fotointerruptor (KY-010)
sensor = Pin(15, Pin.IN)

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("ky010_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos del sensor por MQTT
def publish_data(client, last_value):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return last_value
    
    try:
        value = sensor.value()
        if value != last_value:
            payload = str(value)  # Convertir el valor a string
            client.publish(mqtt_topic, payload)
            print("Datos enviados:", payload)
            return value  # Actualizar último valor enviado
        else:
            print("Valor sin cambios, no se envía")
            return last_value
    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)
        return last_value

# Main
connect_wifi()
client = connect_mqtt()

last_value = None  # Variable para almacenar el último valor del sensor

while True:
    last_value = publish_data(client, last_value)
    time.sleep(1)