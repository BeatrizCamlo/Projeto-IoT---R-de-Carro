from machine import Pin, I2C, PWM
import utime
import network
import ujson
from umqtt.simple import MQTTClient
import lcd_api
import i2c_lcd
from config.py import ADAFRUIT_AIO_USERNAME, ADAFRUIT_AIO_KEY, ADAFRUIT_AIO_URL, FEED_NAME

# ==== Configurações Wi-Fi ====
SSID = "Wokwi-GUEST"
PASSWORD = ""

# ==== Configurações MQTT (Adafruit IO) ====

# ==== Configuração de pinos ====

# Sensor ultrassônico
trig = Pin(23, Pin.OUT)
echo = Pin(22, Pin.IN)

# LEDs
led_verde = Pin(5, Pin.OUT)
led_amarelo = Pin(4, Pin.OUT)
led_vermelho = Pin(2, Pin.OUT)

# Buzzer
buzzer = PWM(Pin(14))

# LCD via I2C
i2c = I2C(0, scl=Pin(25), sda=Pin(26))
lcd = i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)

# ==== Funções ====

def conecta_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando-se ao Wi-Fi", end="")
    while not wlan.isconnected():
        print(".", end="")
        utime.sleep(0.5)
    print(" Conectado!")
    print("IP:", wlan.ifconfig()[0])

def medir_distancia():
    trig.value(0)
    utime.sleep_us(200)
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)

    timeout = utime.ticks_add(utime.ticks_us(), 1000000)  # 1 segundo timeout

    while echo.value() == 0:
        if utime.ticks_diff(timeout, utime.ticks_us()) <= 0:
            return -1
    inicio = utime.ticks_us()

    while echo.value() == 1:
        if utime.ticks_diff(timeout, utime.ticks_us()) <= 0:
            return -1
    fim = utime.ticks_us()

    duracao = utime.ticks_diff(fim, inicio)
    distancia_cm = (duracao / 2) / 29.1
    return round(distancia_cm, 2)

def conecta_mqtt():
    client_id = "esp32_" + str(utime.ticks_ms())  # gera ID único
    client = MQTTClient(client_id, ADAFRUIT_AIO_URL,
                        user=ADAFRUIT_AIO_USERNAME,
                        password=ADAFRUIT_AIO_KEY,
                        keepalive=60)
    client.connect()
    print("Conectado ao Adafruit IO MQTT!")
    return client

def atualizar_display_e_leds(dist):
    lcd.clear()
    if dist == -1:
        lcd.putstr("Erro na leitura")
        led_verde.value(0)
        led_amarelo.value(0)
        led_vermelho.value(0)
        buzzer.duty(0)
        return

    lcd.putstr("Dist: {:.1f} cm".format(dist))

    if dist > 300:
        lcd.putstr("\nDistancia segura.")
        led_verde.value(1)
        led_amarelo.value(0)
        led_vermelho.value(0)
        buzzer.duty(0)
    elif dist > 50:
        lcd.putstr("\nDist. arriscada!")
        led_verde.value(0)
        led_amarelo.value(1)
        led_vermelho.value(0)
        buzzer.duty(0)
    else:
        lcd.putstr("\nDistancia critica")
        led_verde.value(0)
        led_amarelo.value(0)
        led_vermelho.value(1)
        buzzer.freq(1000)
        buzzer.duty(200)

def loop_principal():
    conecta_wifi()
    mqtt = conecta_mqtt()

    while True:
        try:
            dist = medir_distancia()
            print("Distância:", dist, "cm")
            mqtt.publish(FEED, str(dist))

            atualizar_display_e_leds(dist)

            mqtt.ping()          # Mantém conexão viva
            utime.sleep(2)  # Envia a cada 2 segundos


        except OSError as e:
            print("Erro MQTT, tentando reconectar:", e)
            try:
                mqtt.disconnect()
            except:
                pass
            utime.sleep(5)       # Espera um pouco antes de tentar reconectar
            mqtt = conecta_mqtt()  # Reconnect

try:
    loop_principal()
except Exception as e:
    print("Erro fatal:", e)
