import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.187.101"  # Nueva IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/sensores"  # Nuevo tema

# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# Configuración del sensor de temperatura (KY-028 AO conectado a GPIO 34)
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)  # Permite leer valores de 0 a 3.3V

# Función para leer la temperatura
def leer_temperatura():
    valor = sensor.read()  # Leer valor analógico (0 - 4095)
    voltaje = (valor / 4095.0) * 3.3  # Convertir a voltaje
    temperatura = (voltaje - 0.5) * 100  # Aproximación (ajustar si es necesario)
    return temperatura

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("temperature_sensor_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Función para enviar datos de temperatura por MQTT
def publish_data(client, last_temp, temp_threshold=3.0):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return last_temp
    
    try:
        temperatura = leer_temperatura()  # Leer la temperatura
        # Solo enviar si el cambio en temperatura es mayor que el umbral
        if abs(temperatura - last_temp) >= temp_threshold:  
            payload = str(temperatura)  # Convertir la temperatura a string
            client.publish(mqtt_topic, payload)
            print(f"Datos enviados: {payload} °C")
            return temperatura  # Guardar nueva temperatura
        return last_temp
    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)
        return last_temp

# Main
connect_wifi()
client = connect_mqtt()

last_temp = leer_temperatura()  # Obtener la temperatura inicial

while True:
    last_temp = publish_data(client, last_temp, temp_threshold=3.0)  # Cambiar el umbral a 3°C
    time.sleep(5)  # Enviar datos cada 5 segundos, si es necesario
