import time
from machine import Pin
from umqtt.simple import MQTTClient
import network

# Configuración de pines
sensor = Pin(15, Pin.IN)  # Sensor de inclinación (entrada digital en GPIO15)
led = Pin(2, Pin.OUT)     # LED (salida en GPIO2)

# Configuración de la red WiFi
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/inclinacionLed"

# Función para conectar al WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a la red WiFi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Conexión WiFi establecida. Dirección IP:", wlan.ifconfig()[0])

# Función para configurar MQTT
def connect_mqtt():
    client = MQTTClient("esp32", MQTT_BROKER)
    client.connect()
    print("Conectado al servidor MQTT")
    return client

# Conectar al WiFi
connect_wifi()

# Conectar al servidor MQTT
mqtt_client = connect_mqtt()

# Variable para almacenar el último estado del sensor
last_sensor_state = -1  # Inicializamos con un valor diferente

while True:
    sensor_state = sensor.value()  # Leer el estado del sensor
    
    # Compara el nuevo estado con el último
    if sensor_state != last_sensor_state:
        print("Sensor State:", sensor_state)  # Imprimir el estado del sensor (para depuración)
        
        # Publica el estado en el servidor MQTT solo si cambia
        mqtt_client.publish(MQTT_TOPIC, str(sensor_state))
        
        # Actualiza el último estado
        last_sensor_state = sensor_state

        # Controlar el LED
        if sensor_state == 0:  # Si el sensor detecta inclinación (estado LOW)
            led.value(1)  # Enciende el LED
        else:
            led.value(0)  # Apaga el LED
    
    time.sleep(0.1)  # Retardo para evitar lecturas demasiado rápidas
