from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

# Configurar los pines PWM
red = PWM(Pin(15), freq=1000)  # Rojo en GPIO 15
green = PWM(Pin(2), freq=1000)  # Verde en GPIO 2
blue = PWM(Pin(4), freq=1000)  # Azul en GPIO 4


# Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.187.101"
MQTT_TOPIC = "cecr/actuadores"

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




# Función para cambiar colores (valores de 0 a 1023)
def set_color(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)

# Ciclo de prueba cambiando colores
while True:
    set_color(1023, 0, 0)  # Rojo
    color = 1
    client.publish(MQTT_TOPIC, str(color))
    print("",color)
    time.sleep(5)
    
    set_color(0, 1023, 0)  # Verde
    color = 2
    client.publish(MQTT_TOPIC, str(color))
    print("",color)
    time.sleep(5)
    
    set_color(0, 0, 1023)  # Azul
    color = 3
    client.publish(MQTT_TOPIC, str(color))
    print("",color)
    time.sleep(5)
    
    set_color(1023, 1023, 0)  # Amarillo
    color = 4
    client.publish(MQTT_TOPIC, str(color))
    print("", color)
    time.sleep(5)
  
    set_color(0, 1023, 1023)  # Cyan
    color = 5
    client.publish(MQTT_TOPIC, str(color))
    print("", color)
    time.sleep(5)
  
    set_color(1023, 0, 1023)  # Magenta
    color = 6
    client.publish(MQTT_TOPIC, str(color))
    print("", color)
    time.sleep(5)
  
    set_color(1023, 1023, 1023)  # Blanco
    color = 7
    client.publish(MQTT_TOPIC, str(color))
    print("", color)
    time.sleep(5)
  
    set_color(0, 0, 0)  # Apagar
    color = 0
    client.publish(MQTT_TOPIC, str(color))
    print("", color)
    time.sleep(5)