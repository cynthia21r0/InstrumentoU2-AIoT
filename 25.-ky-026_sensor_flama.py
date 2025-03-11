import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.228.100"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/flama"  # Nuevo topic para el sensor de flama

# Configuración del sensor KY-026 (Flama) en GPIO34
flame_sensor = ADC(Pin(34))
flame_sensor.atten(ADC.ATTN_11DB)  # Configura el rango completo (0-4095)

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
        client = MQTTClient("flame_sensor_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos por MQTT
def publish_data(client, valor):
    try:
        mensaje = str(valor)
        client.publish(mqtt_topic, mensaje)
        print("Datos enviados:", mensaje)
    except Exception as e:
        print("Error al enviar datos MQTT:", e)

# Main
connect_wifi()
client = connect_mqtt()

valor_anterior = flame_sensor.read()  # Valor inicial

while True:
    valor_actual = flame_sensor.read()  # Leer el sensor

    if abs(valor_actual - valor_anterior) > 50:  # Solo enviar si cambia más de 50 unidades
        publish_data(client, valor_actual)
        valor_anterior = valor_actual  # Actualizar el estado previo
    
    time.sleep(0.5)  # Pequeña espera para evitar spam
