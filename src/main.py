from machine import Pin, I2C, PWM
import utime
import lcd_api
import i2c_lcd

# --- Configuração dos pinos ---

# Ultrassônico
trig = Pin(27, Pin.OUT)
echo = Pin(26, Pin.IN)

# LEDs
led_verde = Pin(0, Pin.OUT)
led_amarelo = Pin(1, Pin.OUT)
led_vermelho = Pin(2, Pin.OUT)

# Buzzer com PWM para controlar som
buzzer = PWM(Pin(16))

# I2C para LCD 2004 (pinos 6 = SDA, 7 = SCL)
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

# Opcional: escanear I2C para descobrir o endereço do LCD
# enderecos = i2c.scan()
# print("Endereços I2C encontrados:", [hex(a) for a in enderecos])

# Configure o endereço correto aqui, exemplo 0x27 ou 0x3F
lcd_addr = 0x27
lcd = i2c_lcd.I2cLcd(i2c, lcd_addr, 4, 20)

# --- Função para medir distância com timeout ---
def medir_distancia():
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(10)
    trig.low()

    timeout = utime.ticks_us() + 1000000  # timeout 1 segundo

    # Espera echo subir
    while echo.value() == 0:
        if utime.ticks_us() > timeout:
            return -1

    pulse_start = utime.ticks_us()

    # Espera echo cair
    while echo.value() == 1:
        if utime.ticks_us() > timeout:
            return -1

    pulse_end = utime.ticks_us()

    duracao = utime.ticks_diff(pulse_end, pulse_start)
    distancia = (duracao * 0.0343) / 2  # cm
    return distancia

# --- Função para buzzer tocar ---
def buzzer_tocar(frequencia=1000, duracao=500):
    buzzer.freq(frequencia)
    buzzer.duty_u16(30000)  # volume
    utime.sleep_ms(duracao)
    buzzer.duty_u16(0)

# --- Loop principal ---
while True:
    dist = medir_distancia()
    lcd.clear()

    if dist == -1:
        msg = "Erro na medicao"
        print(msg)
        lcd.putstr(msg)
        # Desliga tudo
        led_vermelho.off()
        led_amarelo.off()
        led_verde.off()
        buzzer.duty_u16(0)
    else:
        msg_dist = "Distancia: {:.1f} cm".format(dist)
        print(msg_dist)
        lcd.putstr(msg_dist + "\n")

        if dist < 10:
            led_vermelho.on()
            led_amarelo.off()
            led_verde.off()
            buzzer_tocar(1500, 200)
            lcd.putstr("PERIGO!     ")
            print("PERIGO!")
        elif dist < 30:
            led_vermelho.off()
            led_amarelo.on()
            led_verde.off()
            buzzer_tocar(1000, 100)
            lcd.putstr("Atenção     ")
            print("Atenção")
        else:
            led_vermelho.off()
            led_amarelo.off()
            led_verde.on()
            buzzer.duty_u16(0)
            lcd.putstr("OK          ")
            print("OK")

    utime.sleep(0.5)
