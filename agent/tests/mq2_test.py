#!/usr/bin/env python3
import sys
import time
from agent.devices import mq

try:
    print("Press CTRL+C to abort.")

    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" %
                         (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nAbort by user")
