import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/tactilMetal"

# Función para conectar a WiFi con reintentos
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
        print("Conectado a WiFi! IP:", wifi.ifconfig()[0])
    else:
        print("Error: No se pudo conectar a WiFi")

# Función para conectar a MQTT con manejo de errores
def conectar_mqtt():
    try:
        client = MQTTClient("ESP32", MQTT_BROKER)
        client.connect()
        print("Conectado a MQTT!")
        return client
    except Exception as e:
        print("Error al conectar a MQTT:", e)
        return None

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_mqtt()

# Configuración del sensor KY-036 (solo lectura analógica)
pin_analogico = machine.ADC(machine.Pin(34))  # Entrada analógica en GPIO 34
pin_analogico.atten(machine.ADC.ATTN_11DB)   # Ajuste para leer de 0 a 3.3V

# Bucle principal para enviar datos por MQTT
while True:
    valor_analogico = pin_analogico.read()  # Leer el valor (0 - 4095)
    
    print(f"Valor analógico: {valor_analogico}")
    
    if client:  # Publicar solo si hay conexión MQTT
        client.publish(MQTT_TOPIC, str(valor_analogico).encode())

    time.sleep(1)  # Enviar cada segundo
