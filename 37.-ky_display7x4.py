import tm1637
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# 📡 Configuración WiFi
SSID = "Ross"
PASSWORD = "chaeunwoo123"

# 🌍 Configuración MQTT
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/display"

# 📌 Pines TM1637
CLK = 14  # GPIO14
DIO = 27  # GPIO27

# 🔌 Inicializar display
tm = tm1637.TM1637(clk=CLK, dio=DIO)
tm.set_brightness(5)

# 📶 Conectar a WiFi
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    intentos = 0
    while not wifi.isconnected() and intentos < 10:
        print("Conectando a WiFi...")
        time.sleep(1)
        intentos += 1

    if wifi.isconnected():
        print("✅ Conectado a WiFi, IP:", wifi.ifconfig()[0])
    else:
        print("❌ No se pudo conectar a WiFi")

# 📡 Conectar MQTT
def conectar_mqtt():
    try:
        client = MQTTClient("ESP32", MQTT_BROKER)
        client.connect()
        print("✅ Conectado a MQTT!")
        return client
    except Exception as e:
        print("❌ Error al conectar a MQTT:", e)
        return None

# 🚀 Conectar WiFi y MQTT
conectar_wifi()
mqtt = conectar_mqtt()

# 🔢 Contador en el display y envío MQTT
for i in range(10000):
    tm.number(i)  # Mostrar número en el display
    print(f"Mostrando: {i}")  # Imprimir en consola

    if mqtt:
        mqtt.publish(MQTT_TOPIC, str(i))  # Enviar número al broker MQTT
        print(f"📡 Enviado a MQTT: {i}")

    time.sleep(0.5)

# 📌 Mostrar "Hi" al final
tm.show("HI  ")
time.sleep(2)

print("✅ Prueba completada")