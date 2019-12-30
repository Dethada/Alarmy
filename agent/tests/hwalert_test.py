#!/usr/bin/env python3
from utils import HWAlert
from time import sleep

hwalert = HWAlert(21)
hwalert.on()
input('Waiting: ')
hwalert.off()