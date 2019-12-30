#!/usr/bin/env python3
from utils import HWAlert
from time import sleep

hwalert = HWAlert(21)
# hwalert.on()
# input('Waiting: ')
# hwalert.off()
hwalert.run_for('ABC', 10)
sleep(2)
for i in range(5):
    print(i)
hwalert.kill()
# hwalert.thread.join()