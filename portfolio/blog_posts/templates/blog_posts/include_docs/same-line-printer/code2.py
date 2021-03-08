printer = SameLinePrinter()
for i in range(1, 101):
    time.sleep(1)
    printer.print_line("Test: {:>3} / 100".format(i))
