import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import utime

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.187.101"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/actuadores"

# Definir el GPIO donde está conectado el KY-008 (láser)
laser = Pin(4, Pin.OUT)  # Cambia "4" por otro GPIO si es necesario

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
        client = MQTTClient("laser_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar estado del láser a MQTT
def publish_laser_status(client, status):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return
    try:
        # Usamos 1 para láser encendido y 0 para láser apagado
        payload = str(status)  # Convertimos el valor a cadena
        # Usamos retain=True para asegurarnos de que el mensaje se mantenga en el broker
        client.publish(mqtt_topic, payload, retain=True)
        print("Estado del láser enviado:", payload)
    except Exception as e:
        print("Error al enviar datos MQTT:", e)

# Main
connect_wifi()
client = connect_mqtt()

while True:
    # Encender el láser (enviar 1)
    laser.value(01)  # Encender el láser
    publish_laser_status(client, 01)  # Enviar estado "1" (láser encendido)
    print("Láser ENCENDIDO")
    utime.sleep(1)

    # Apagar el láser (enviar 0)
    laser.value(10)  # Apagar el láser
    publish_laser_status(client, 10)  # Enviar estado "0" (láser apagado)
    print("Láser APAGADO")
    utime.sleep(1)