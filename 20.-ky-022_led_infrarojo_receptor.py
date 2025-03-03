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
mqtt_topic = "cecr/sensores"

# Configuración del sensor KY-022
sensor_ir = Pin(15, Pin.IN)  # Cambia el GPIO si es necesario

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
        client = MQTTClient("sensor_ir_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos por MQTT solo cuando el estado cambie
def publish_data(client, estado_ir):
    try:
        payload = str(estado_ir)  # Convertir el valor a string
        client.publish(mqtt_topic, payload)
        print("Datos enviados:", payload)
    except Exception as e:
        print("Error al enviar datos MQTT:", e)

# Main
connect_wifi()
client = connect_mqtt()

estado_anterior = sensor_ir.value()  # Estado inicial

while True:
    estado_actual = sensor_ir.value()
    
    if estado_actual != estado_anterior:  # Solo envía si el estado cambia
        publish_data(client, estado_actual)
        estado_anterior = estado_actual  # Actualizar el estado previo
    
    time.sleep(0.1)  # Pequeña espera para evitar falsos positivos