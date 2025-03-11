import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.228.100"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/linea"  # Nuevo topic para el KY-033

# Configuración del sensor KY-033
sensor_ky033 = Pin(34, Pin.IN)  # OUT del KY-033 conectado al GPIO 34

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
        client = MQTTClient("ky033_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos por MQTT
def publish_data(client, estado):
    try:
        mensaje = str(estado)  # Enviar solo "0" o "1"
        client.publish(mqtt_topic, mensaje)
        print("Datos enviados:", mensaje)
    except Exception as e:
        print("Error al enviar datos MQTT:", e)

# Main
connect_wifi()
client = connect_mqtt()

while True:
    estado_actual = sensor_ky033.value()  # Leer estado del sensor
    publish_data(client, estado_actual)  # Enviar el dato cada 5 segundos
    time.sleep(5)  # Esperar 5 segundos antes de la siguiente lectura
