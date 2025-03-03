from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.228.100"
MQTT_TOPIC = "cecr/sensors"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("✅ Conectado a MQTT!")

# Configurar el KY-021 en el GPIO26
reed_switch = Pin(26, Pin.IN, Pin.PULL_UP)  # Pull-up interno

while True:
    estado = 1 if reed_switch.value() == 0 else 0  # 1 = imán detectado, 0 = sin imán
    
    # Mostrar el estado en la terminal
    print(f"Estado del sensor: {estado}")

    # Enviar el estado a MQTT
    client.publish(MQTT_TOPIC, str(estado).encode())  # Convertimos a string en bytes para MQTT

    time.sleep(2)  # Enviar datos cada 2 segundos