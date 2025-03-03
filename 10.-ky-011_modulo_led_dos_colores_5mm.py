import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.187.101"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/actuadores"

# Configuración del LED KY-011
pin_led = Pin(4, Pin.OUT)  # GPIO para el LED

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

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("led_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar estado del LED a MQTT
def publish_led_status(client, status):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return
    try:
        # Usamos 1 para LED encendido y 0 para LED apagado
        payload = str(status)  # Convertimos el valor a cadena
        # Usamos retain=True para asegurarnos de que el mensaje se mantenga en el broker
        client.publish(mqtt_topic, payload, retain=True)
        print("Estado del LED enviado:", payload)
    except Exception as e:
        print("Error al enviar datos MQTT:", e)

# Main
connect_wifi()
client = connect_mqtt()

while True:
    # Encender LED (enviar 1)
    pin_led.value(1)  # LED encendido
    publish_led_status(client, 1)  # Enviar estado "1" (LED encendido)
    time.sleep(5)

    # Apagar LED (enviar 0)
    pin_led.value(0)  # LED apagado
    publish_led_status(client, 0)  # Enviar estado "0" (LED apagado)
    time.sleep(5)