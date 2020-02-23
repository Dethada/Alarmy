#!/usr/bin/env python3
import json
from time import sleep
from gpiozero import Buzzer
from gpiozero import MotionSensor
from nanpy import ArduinoApi
from nanpy import SerialManager
from rpi_lcd import LCD
import adafruit_matrixkeypad
import board
from digitalio import DigitalInOut

with open('config.json') as json_file:
    config = json.load(json_file)

BUZZER_PIN = config['BUZZER_PIN']
MQ2_PIN = config['MQ2_APIN']
LM35_PIN = config['LM35_PIN']
MOTION_PIN = config['MOTION_PIN']


def nanpy_connect():
    connection = SerialManager(device='/dev/ttyUSB0')
    arduinoObject = ArduinoApi(connection=connection)
    return arduinoObject


def test_buzzer():
    print('Testing buzzer...')
    bz = Buzzer(BUZZER_PIN)
    bz.on()
    sleep(1)
    bz.off()
    ans = input('Heard a buzz? y/n: ')
    return ans == 'y'


def test_lcd():
    print('Testing LCD...')
    lcd = LCD()
    lcd.text('Works', 1)
    ans = input('Is Works printed on the LCD? y/n: ')
    lcd.clear()
    return ans == 'y'


def test_motionsensor():
    print('Testing motion sensor...')
    pir = MotionSensor(MOTION_PIN, sample_rate=5, queue_len=1)
    print('Activate the motion sensor')
    pir.wait_for_motion()
    return True


def test_keypad():
    # 4x4 matrix keypad
    rows = [DigitalInOut(x)
            for x in (board.D4, board.D17, board.D27, board.D22)]
    cols = [DigitalInOut(x)
            for x in (board.D18, board.D23, board.D24, board.D25)]
    keys = (('1', '2', '3', 'A'),
            ('4', '5', '6', 'B'),
            ('7', '8', '9', 'C'),
            ('*', '0', '#', 'D'))

    keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

    print('Press 1234A')
    entered_keys = ''
    while True:
        keys = keypad.pressed_keys
        if keys:
            if keys[0] == '*':
                print('Done')
                return entered_keys == '1234A'
            elif keys[0] == 'C':
                entered_keys = ''
            else:
                entered_keys += keys[0]
            print("Pressed: ", entered_keys)
            sleep(0.2)


def test_mq2():
    print('Testing MQ2...')
    arduino = nanpy_connect()
    arduino.pinMode(MQ2_PIN, arduino.INPUT)
    value = arduino.analogRead(MQ2_PIN)
    print('Gas Value: {}'.format(value))
    ans = input('Valid value? y/n: ')
    return ans == 'y'


def test_lm35():
    print('Testing LM35...')
    arduino = nanpy_connect()
    arduino.pinMode(LM35_PIN, arduino.INPUT)
    value = arduino.analogRead(LM35_PIN)
    temp = (value * 500) / 1024
    print('Temp: {0:.2f} C'.format(temp))
    ans = input('Valid value? y/n: ')
    return ans == 'y'


def main():
    buzzer_result = test_buzzer()
    lcd_result = test_lcd()
    motion_result = test_motionsensor()
    keypad_result = test_keypad()
    mq2_result = test_mq2()
    lm35_result = test_lm35()
    print('Results:\nBuzzer: {}\nLCD: {}\nMotion Sensor: {}\nKeypad: {}\nMQ2: {}\nLM35: {}'.format(
        buzzer_result, lcd_result, motion_result, keypad_result, mq2_result, lm35_result))


if __name__ == '__main__':
    main()
