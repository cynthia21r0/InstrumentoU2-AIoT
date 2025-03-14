import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep, ticks_ms, ticks_diff

# --- Configuración WiFi ---
WIFI_SSID = "Ross"
WIFI_PASSWORD = "chaeunwoo123"

# --- Configuración MQTT ---
MQTT_BROKER = "192.168.156.100"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "ESP32_KY040"
MQTT_TOPIC = "cecr/encoder"
MQTT_PORT = 1883

# --- Configuración de pines para el encoder KY-040 ---
clk = Pin(14, Pin.IN, Pin.PULL_UP)  # Pin CLK
dt  = Pin(27, Pin.IN, Pin.PULL_UP)  # Pin DT
sw  = Pin(25, Pin.IN, Pin.PULL_UP)  # Botón (SW)

# --- Función para conectar a WiFi ---
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi conectada!")

# --- Función para conectarse al broker MQTT ---
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID,
                        MQTT_BROKER,
                        port=MQTT_PORT,
                        user=MQTT_USER,
                        password=MQTT_PASSWORD,
                        keepalive=0)
    client.connect()
    print("Conectado a %s en el tópico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Conectar a WiFi y al broker MQTT
conectar_wifi()
client = conectar_mqtt()

# Variables para el control del encoder
last_clk = clk.value()       # Guarda el estado anterior del pin CLK
last_sw  = sw.value()        # Guarda el estado anterior del botón
debounce_time = 50           # Tiempo de debounce en milisegundos
last_sw_time = ticks_ms()    # Marca de tiempo para el botón

# Bucle principal: detecta rotación y pulsación del botón
while True:
    current_time = ticks_ms()
    
    # --- Detección de rotación ---
    current_clk = clk.value()
    if current_clk != last_clk:
        # Detectamos un cambio en CLK; se toma el flanco descendente
        if current_clk == 0:
            # Si en el flanco descendente, se compara DT con CLK para determinar la dirección
            if dt.value() == 1:
                direction = "CW"   # Rotación en el sentido de las agujas del reloj
            else:
                direction = "CCW"  # Rotación contraria
            print("Rotación:", direction)
            client.publish(MQTT_TOPIC, direction)
        last_clk = current_clk  # Actualizamos el estado de CLK
    
    # --- Detección de pulsación del botón ---
    current_sw = sw.value()
    if current_sw != last_sw and ticks_diff(current_time, last_sw_time) > debounce_time:
        if current_sw == 0:
            print("Botón presionado - Enviando 1")
            client.publish(MQTT_TOPIC, "1")  # Envía "1" cuando se presiona el botón
        last_sw = current_sw
        last_sw_time = current_time

    sleep(0.01)
