# lcd_api.py

import time

class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.backlight = True

    def clear(self):
        self.hal_write_command(0x01)
        self.cursor_x = 0
        self.cursor_y = 0
        time.sleep_ms(2)

    def move_to(self, row, col):
        self.cursor_y = row
        self.cursor_x = col
        addr = col + 0x40 * row
        self.hal_write_command(0x80 | addr)

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.cursor_y += 1
                self.cursor_x = 0
                self.move_to(self.cursor_y, self.cursor_x)
            else:
                self.hal_write_data(ord(char))
                self.cursor_x += 1
                if self.cursor_x >= self.num_columns:
                    self.cursor_x = 0
                    self.cursor_y += 1
                    if self.cursor_y < self.num_lines:
                        self.move_to(self.cursor_y, self.cursor_x)

    def show_cursor(self):
        self.hal_write_command(0x0E)

    def hide_cursor(self):
        self.hal_write_command(0x0C)

    def blink_cursor_on(self):
        self.hal_write_command(0x0F)

    def blink_cursor_off(self):
        self.hal_write_command(0x0C)

    def display_on(self):
        self.hal_write_command(0x0C)

    def display_off(self):
        self.hal_write_command(0x08)

    def backlight_on(self):
        self.backlight = True
        self.hal_backlight_on()

    def backlight_off(self):
        self.backlight = False
        self.hal_backlight_off()

    # As funções abaixo devem ser implementadas pela subclasse
    def hal_write_command(self, cmd): raise NotImplementedError

    def hal_write_data(self, data): raise NotImplementedError

    def hal_backlight_on(self): raise NotImplementedError

    def hal_backlight_off(self): raise NotImplementedError
