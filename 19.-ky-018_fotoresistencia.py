from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
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

# Configurar el pin analógico donde está conectado el LDR
ldr = ADC(Pin(34))  # Usa el pin adecuado
ldr.atten(ADC.ATTN_11DB)  # Rango de 0-3.3V (0-4095)

while True:
    # Leer el valor analógico del LDR
    valor_ldr = ldr.read()

    # Mostrar el valor en la terminal
    print(f"Valor LDR (ADC): {valor_ldr}")

    # Clasificación del nivel de luz
    if valor_ldr < 1000:
        print("Mucha luz")
    else:
        print("Poca luz")
        client.publish(MQTT_TOPIC, str(valor_ldr))

    time.sleep(5)  # Espera de 1 segundo