import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# 📡 Configuración WiFi
SSID = "Ross"
PASSWORD = "chaeunwoo123"

# 🌍 Configuración MQTT
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/mq2"

# 📶 Conectar a WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Conectando a WiFi...")
        time.sleep(1)
    print("Conectado a WiFi:", wlan.ifconfig())

# 📡 Conectar a MQTT
def conectar_mqtt():
    cliente = MQTTClient("ESP32_MQ2", MQTT_BROKER)
    cliente.connect()
    print("Conectado a MQTT")
    return cliente

# 🔍 Configurar el sensor MQ-2
mq2 = ADC(Pin(34))
mq2.atten(ADC.ATTN_11DB)  # Permite leer hasta 3.3V

# 📶 Conectar a WiFi y MQTT
conectar_wifi()
cliente_mqtt = conectar_mqtt()

# 🔄 Variables para detectar cambios
umbral_cambio = 40  # Solo enviar si la diferencia es de 40 o más
ultimo_enviado = mq2.read()

while True:
    valor_actual = int(mq2.read())  # Convertir a entero explícitamente

    # 📊 Enviar solo si la diferencia es mayor o igual a 40
    if abs(valor_actual - ultimo_enviado) >= umbral_cambio:
        mensaje = str(valor_actual)  # Enviar el número como string
        cliente_mqtt.publish(MQTT_TOPIC, mensaje)
        print("📤 Enviado a MQTT:", mensaje)
        ultimo_enviado = valor_actual  # Actualizar el último valor enviado

    time.sleep(1)  # Evitar envíos constantes
