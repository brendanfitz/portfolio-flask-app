import sys
import time

class SameLinePrinter:

    def __init__(self, previous_line_length=0):
        self.previous_line_length = previous_line_length

    def print_line(self, line):
        print('\r' + ' ' * self.previous_line_length + '\r', end='')
        print(line, end='')
        sys.stdout.flush()
        self.previous_line_length = len(line)
