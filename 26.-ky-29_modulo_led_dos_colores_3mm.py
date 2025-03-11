import machine
import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.228.100"
MQTT_TOPIC = "cecr/led2colores3mm"


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


# Configurar el pin del LED bicolor
led_red = Pin(14, Pin.OUT)  # Pin para el LED rojo
led_green = Pin(13, Pin.OUT)  # Pin para el LED verde


while True:
    # Encender LED rojo y apagar LED verde
    led_red.value(1)  # Rojo encendido
    led_green.value(0)  # Verde apagado
    led = 1
    client.publish(MQTT_TOPIC, str(led))
    print("Rojo")
    time.sleep(3)  # Esperar 3 segundos
    
    # Apagar LED rojo y encender LED verde
    led_red.value(0)  # Rojo apagado
    led_green.value(2)  # Verde encendido
    led = 2
    client.publish(MQTT_TOPIC, str(led))
    print("Verde")
    time.sleep(3)  # Esperar 3 segundos