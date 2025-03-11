7 colores: import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo"
MQTT_BROKER = "192.168.228.100"
MQTT_TOPIC = "cecr/led7colores"


# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("Conectado a MQTT!")


# Definir el pin del LED (control de color rojo en este caso)
R = machine.Pin(2, machine.Pin.OUT)  # Cambia al pin que estés utilizando

# Inicializar la comunicación serial
print("Ejemplo - 7 colores")

# Bucle principal
while True:
    R.value(1)  # Encender el LED (HIGH)
    client.publish(MQTT_TOPIC, "1")
    print("Led encendido")
    time.sleep(5)  # Mantenerlo encendido durante 5 segundos
    R.value(0)  # Apagar el LED (LOW)
    print("Led Apagado")
    time.sleep(5)  # Mantenerlo apagado durante 1 segundo