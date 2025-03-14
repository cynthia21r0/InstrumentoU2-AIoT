import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Configuración WiFi
WIFI_SSID = "Ross"
WIFI_PASSWORD = "chaeunwoo123"

# Configuración MQTT
MQTT_BROKER = "192.168.156.100"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "ESP32_JOYSTICK"
MQTT_TOPIC = "cecr/joys"
MQTT_PORT = 1883

# Configuración de los pines ADC para VRX y VRY
vrx = ADC(Pin(34))  # Eje X
vry = ADC(Pin(35))  # Eje Y
vrx.atten(ADC.ATTN_11DB)  # Configurar rango de 0-3.3V
vry.atten(ADC.ATTN_11DB)

# Configuración del botón SW como entrada digital con pull-down
sw = Pin(32, Pin.IN, Pin.PULL_DOWN)

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi conectada!")

# Función para conectarse al broker MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.connect()
    print("Conectado a %s en el tópico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

# Contador para alternar el envío de valores
contador = 0

# Bucle principal: lee el joystick y envía datos por MQTT
while True:
    x_value = vrx.read()  # Lectura del eje X (0-4095)
    y_value = vry.read()  # Lectura del eje Y (0-4095)
    sw_state = sw.value() # Estado del botón (1 = presionado, 0 = no presionado)

    # Alternar entre los valores en cada iteración
    if contador % 3 == 0:
        dato_enviar = x_value
        print("Enviando X:", dato_enviar)
    elif contador % 3 == 1:
        dato_enviar = y_value
        print("Enviando Y:", dato_enviar)
    else:
        dato_enviar = sw_state
        print("Enviando Botón:", dato_enviar)

    # Publicar el dato en el mismo tópico
    client.publish(MQTT_TOPIC, str(dato_enviar))

    # Incrementar el contador y esperar 1 segundo
    contador += 1
    sleep(4)
