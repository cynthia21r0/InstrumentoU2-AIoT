import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "Ross"
PASSWORD = "chaeunwoo123"
MQTT_BROKER = "192.168.156.100"
MQTT_TOPIC = "cecr/pulso"

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

# Configuración del sensor de pulso KY-039
sensor_pulso = machine.Pin(15, machine.Pin.IN)

# Bucle principal
while True:
    conteo = 0
    inicio = time.ticks_ms()
    ultimo_pulso = inicio
    estado_anterior = sensor_pulso.value()

    # Medir pulsaciones en 10 segundos
    while time.ticks_diff(time.ticks_ms(), inicio) < 10000:  
        estado_actual = sensor_pulso.value()
        if estado_anterior == 1 and estado_actual == 0:  # Flanco descendente
            if time.ticks_diff(time.ticks_ms(), ultimo_pulso) > 250:  # Debounce
                conteo += 1
                ultimo_pulso = time.ticks_ms()
                print("Pulso detectado. Total:", conteo)
        estado_anterior = estado_actual
        time.sleep(0.01)

    bpm = conteo * 6  # BPM = latidos en 10s * 6
    print("BPM:", bpm)

    if client:  # Solo publicar si hay conexión MQTT
        client.publish(MQTT_TOPIC, str(bpm).encode())

    time.sleep(2)  # Esperar antes de la próxima medición