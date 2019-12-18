#!/usr/bin/env python3
from gpiozero import MCP3008
from time import sleep

ADC = MCP3008(channel=0)

while True: 
    print(ADC.value)
    sleep(1)
