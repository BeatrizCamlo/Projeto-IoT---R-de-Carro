class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0

    def clear(self):
        self.cursor_x = 0
        self.cursor_y = 0

    def putstr(self, string):
        print(string)

    def move_to(self, col, row):
        self.cursor_x = col
        self.cursor_y = row
