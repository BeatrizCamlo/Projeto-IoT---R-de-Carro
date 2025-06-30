# i2c_lcd.py

from lcd_api import LcdApi
from machine import I2C
import time

# comandos do LCD
LCD_CLR = 0x01
LCD_HOME = 0x02
LCD_ENTRY_MODE_SET = 0x04
LCD_DISPLAY_CONTROL = 0x08
LCD_FUNCTION_SET = 0x20
LCD_SET_DDRAM_ADDR = 0x80

# flags
LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_DECREMENT = 0x00
LCD_DISPLAY_ON = 0x04
LCD_DISPLAY_OFF = 0x00
LCD_CURSOR_ON = 0x02
LCD_CURSOR_OFF = 0x00
LCD_BLINK_ON = 0x01
LCD_BLINK_OFF = 0x00
LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00
LCD_4BIT_MODE = 0x00

class I2cLcd(LcdApi):
    def __init__(self, i2c, address, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = address
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = 0x08
        self._write_byte(0)
        time.sleep_ms(20)
        self._send(0x03 << 4)
        time.sleep_ms(5)
        self._send(0x03 << 4)
        time.sleep_ms(1)
        self._send(0x03 << 4)
        self._send(0x02 << 4)
        self.hal_write_command(LCD_FUNCTION_SET | LCD_2LINE | LCD_5x8DOTS | LCD_4BIT_MODE)
        self.hal_write_command(LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON)
        self.hal_write_command(LCD_CLR)
        time.sleep_ms(2)
        self.hal_write_command(LCD_ENTRY_MODE_SET | LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)

    def hal_write_command(self, cmd):
        self._send(cmd & 0xF0)
        self._send((cmd << 4) & 0xF0)

    def hal_write_data(self, data):
        self._send(data & 0xF0, rs=1)
        self._send((data << 4) & 0xF0, rs=1)

    def hal_backlight_on(self):
        self.backlight = 0x08
        self._write_byte(0)

    def hal_backlight_off(self):
        self.backlight = 0x00
        self._write_byte(0)

    def _write_byte(self, data):
        self.i2c.writeto(self.i2c_addr, bytearray([data | self.backlight]))

    def _send(self, data, rs=0):
        upper = data | (rs << 0) | 0x04
        lower = data | (rs << 0)
        self._write_byte(upper)
        time.sleep_us(50)
        self._write_byte(lower)
        time.sleep_us(50)
