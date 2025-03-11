import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# 🔹 Configuración de la red Wi-Fi
wifi_ssid = "Ross"  # Cambia por tu SSID
wifi_password = "chaeunwoo123"  # Cambia por tu contraseña

# 🔹 Configuración del broker MQTT
mqtt_broker = "192.168.228.100"  # IP del broker
mqtt_port = 1883
mqtt_topic = "cecr/obstaculos"  # Nuevo topic para el sensor KY-032

# 🔹 Configuración del sensor KY-032
sensor = Pin(23, Pin.IN)  # Pin para leer el sensor

# 📡 Función para conectar a Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# 🔗 Función para conectar al broker MQTT
def connect_mqtt():
    try:
        client = MQTTClient("sensor_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# 🔄 Bucle principal
def main():
    # Conectar a Wi-Fi y MQTT
    connect_wifi()
    client = connect_mqtt()

    while client:
        estado = sensor.value()  # Leer estado del sensor KY-032
        mensaje = str(estado)  # Convertir el valor del estado en un string para enviarlo

        try:
            client.publish(mqtt_topic, mensaje)  # Publicar el mensaje en el topic
            print("Datos enviados por MQTT:", mensaje)  # Mostrar el valor enviado
        except Exception as e:
            print("Error al enviar datos MQTT:", e)
        
        time.sleep(2)  # Esperar un poco antes de la siguiente lectura

# Ejecutar el programa
main()