#!/usr/bin/env python3
from hwalert import hwalert
from time import sleep

# hwalert.on('ABC')
# input('Waiting: ')
# hwalert.off()
hwalert.run_for('ABC', 10)
sleep(5)
for i in range(5):
    print(i)
hwalert.stop_alert()