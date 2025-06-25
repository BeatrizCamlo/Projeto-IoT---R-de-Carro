from lcd_api import LcdApi

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        super().__init__(num_lines, num_columns)

    def clear(self):
        super().clear()

    def putstr(self, string):
        super().putstr(string)

    def move_to(self, col, row):
        super().move_to(col, row)
