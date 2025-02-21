import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.187.101"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/sensoresqq"

# Configuración del sensor de sonido (KY-037)
sensor_pin = 34  # GPIO de la ESP32 conectado a OUT del KY-037
sensor = ADC(Pin(sensor_pin))
sensor.atten(ADC.ATTN_11DB)  # Rango hasta 3.6V

# Umbral de cambio para evitar envíos constantes
umbral_cambio = 500  # Ajusta según sea necesario

# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("sensor_sonido_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos solo si hay cambio brusco en el sonido
def publish_data(client, last_value):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return last_value
    
    try:
        value = sensor.read()  # Leer el nivel de sonido (0-4095)
        
        if abs(value - last_value) > umbral_cambio:  # Solo enviar si hay cambio significativo
            payload = str(value)  # Convertir el valor a string
            client.publish(mqtt_topic, payload)
            print("Datos enviados:", payload)
            return value  # Guardar nuevo valor
        
        return last_value
    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)
        return last_value

# Main
connect_wifi()
client = connect_mqtt()

last_value = sensor.read()  # Obtener la lectura inicial del sensor

while True:
    last_value = publish_data(client, last_value)
    time.sleep(0.1)  # Pequeña pausa para evitar saturar la red