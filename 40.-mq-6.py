from machine import Pin, ADC
import network
import time
from umqtt.simple import MQTTClient

# 📡 Configuración WiFi
SSID = "Ross"
PASSWORD = "chaeunwoo123"

# 🌍 Configuración MQTT
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/mq6"

# 📌 Configuración del pin analógico del MQ-6
PIN_MQ6 = 35  # GPIO35 en ESP32
mq6 = ADC(Pin(PIN_MQ6))
mq6.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V

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

# 📌 Lectura del sensor MQ-6
def leer_mq6():
    valor = mq6.read()  # Leer ADC (0-4095)
    voltaje = (valor / 4095) * 3.3  # Convertir a voltios
    print(f"🔍 Lectura: {valor} | Voltaje: {voltaje:.2f}V")
    return valor

# 🔁 Loop principal
while True:
    valor_mq6 = leer_mq6()
    
    if mqtt:
        mensaje = str(valor_mq6)  # Convertir número a string
        mqtt.publish(MQTT_TOPIC, mensaje)  # Enviar por MQTT
        print(f"📡 Enviado a MQTT: {mensaje}")

    time.sleep(2)