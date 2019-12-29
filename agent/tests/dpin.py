#!/usr/bin/env python3
from gpiozero import DigitalInputDevice
from time import sleep

def main():
    dpin = DigitalInputDevice(26, pull_up=True)
    # dpin.when_activated = gas_alert
    # dpin.wait_for_active()
    # print('Alert')
    while True:
        print(dpin.value)
        sleep(1)

if __name__ == "__main__":
    main()