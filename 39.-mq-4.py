from machine import Pin, ADC
import network
import time
from umqtt.simple import MQTTClient

# 📡 Configuración WiFi
SSID = "Ross"
PASSWORD = "chaeunwoo123"

# 🌍 Configuración MQTT
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/mq4"

# 📌 Configuración del pin analógico del MQ-4
PIN_MQ4 = 35  # GPIO35 en ESP32
mq4 = ADC(Pin(PIN_MQ4))
mq4.atten(ADC.ATTN_11DB)  # Rango completo (0-3.3V)

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

# 📌 Lectura del sensor MQ-4
def leer_mq4():
    valor = mq4.read()  # Leer ADC (0-4095)
    voltaje = (valor / 4095) * 3.3  # Convertir a voltios
    print(f"🔍 Lectura: {valor} | Voltaje: {voltaje:.2f}V")
    return valor

# 🔁 Loop principal
while True:
    valor_mq4 = leer_mq4()
    
    if mqtt:
        mensaje = str(valor_mq4)  # Convertir número a string
        mqtt.publish(MQTT_TOPIC, mensaje)  # Enviar por MQTT
        print(f"📡 Enviado a MQTT: {mensaje}")

    time.sleep(2)