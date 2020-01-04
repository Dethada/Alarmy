import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
print('='*32)
for p in ports:
    print(p.hwid, p.description)
    print('='*32)