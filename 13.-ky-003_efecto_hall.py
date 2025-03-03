from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración del sensor KY-003
SENSOR_PIN = 5  # GPIO donde está conectado el sensor
sensor = Pin(SENSOR_PIN, Pin.IN)

# Configuración WiFi
WIFI_SSID = "Ross"
WIFI_PASSWORD = "chaeunwoo123"

# Configuración MQTT
MQTT_CLIENT_ID = "esp32_ky003"
MQTT_BROKER = "192.168.160.100"  # Cambia esto por la IP de tu broker MQTT
MQTT_PORT = 1883
MQTT_TOPIC = "cecr/sensores"

# Función para conectar WiFi
def conectar_wifi():
    print("[INFO] Conectando a WiFi...")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\n[INFO] Conectado a WiFi!")

# Función para conectar MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print(f"[INFO] Conectado a MQTT en {MQTT_BROKER}")
    return client

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

# Estado anterior del sensor
estado_anterior = sensor.value()

# Bucle principal
while True:
    estado_actual = sensor.value()  # Leer el estado del sensor

    if estado_actual != estado_anterior:
        if estado_actual == 0:
            mensaje = "4"  # Detecta imán
        else:
            mensaje = "2"  # No detecta imán

        print(f"[INFO] Enviando: {mensaje}")
        client.publish(MQTT_TOPIC, mensaje.encode())  # Publicar en MQTT

    estado_anterior = estado_actual  # Actualizar estado
    time.sleep(0.2)  # Pequeña pausa para evitar ruido