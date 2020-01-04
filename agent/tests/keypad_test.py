#!/usr/bin/env python3
from hwalert import hwalert
from keypad import check_input
from utils import Thread

hwalert.on('Test')
input_thread=Thread(check_input)