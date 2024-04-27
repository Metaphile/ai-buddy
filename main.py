#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2022/06/28
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime

import random
from enum import Enum

class EyeState(Enum):
    LOOKING_FORWARD = 'o'
    LOOKING_LEFT = '<'
    LOOKING_RIGHT = '>'

class EyelidsState(Enum):
    OPEN = 'o' # this symbol is ignored - we will use the eye state
    CLOSED = '-'

class MouthState(Enum):
    NEUTRAL = '-'
    SMILING = 'v'
    FROWNING = '_'
    AGAPE = 'O'
    SMALL = '.'

FaceState = Enum('FaceState', ['DEFAULT', 'BLINKING', 'WINKING'])

class Face():
    def __init__(self):
        self.left_eyelids_state = EyelidsState.OPEN
        self.left_eye_state = EyeState.LOOKING_FORWARD

        self.right_eyelids_state = EyelidsState.OPEN
        self.right_eye_state = EyeState.LOOKING_FORWARD

        self.mouth_state = MouthState.NEUTRAL

        self.face_state = FaceState.DEFAULT
        self.previous_face_state = self.face_state

    def smile(self):
        # self.left_eyelids_state = EyelidsState.CLOSED
        # self.right_eyelids_state = EyelidsState.CLOSED
        self.mouth_state = MouthState.SMILING
    
    def do_not_smile(self):
        self.mouth_state = MouthState.NEUTRAL
    
    def frown(self):
        self.mouth_state = MouthState.FROWNING
    
    def look_left(self):
        self.left_eye_state = EyeState.LOOKING_LEFT
        self.right_eye_state = EyeState.LOOKING_LEFT
    
    def look_right(self):
        self.left_eye_state = EyeState.LOOKING_RIGHT
        self.right_eye_state = EyeState.LOOKING_RIGHT
    
    def look_forward(self):
        self.left_eye_state = EyeState.LOOKING_FORWARD
        self.right_eye_state = EyeState.LOOKING_FORWARD
    
    def blink(self):
        self.close_eyes()

        self.previous_face_state = self.face_state
        self.face_state = FaceState.BLINKING
    
    def wink(self):
        self.right_eyelids_state = EyelidsState.CLOSED
    
    def do_not_wink(self):
        self.right_eyelids_state = EyelidsState.OPEN
    
    def close_eyes(self):
        self.left_eyelids_state = EyelidsState.CLOSED
        self.right_eyelids_state = EyelidsState.CLOSED

    def update(self):
        if (self.face_state == FaceState.BLINKING):
            self.left_eyelids_state = EyelidsState.OPEN
            self.right_eyelids_state = EyelidsState.OPEN
            self.face_state = self.previous_face_state
    
    def display(self, lcd):
        lcd.setCursor(3, 0)
        lcd.message('$')
        lcd.setCursor(11, 0)
        lcd.message('$')

        # left eye
        lcd.setCursor(5, 0)
        if (self.left_eyelids_state == EyelidsState.CLOSED):
            lcd.message(self.left_eyelids_state.value)
        else:
            lcd.message(self.left_eye_state.value)
        
        # right eye
        lcd.setCursor(9, 0)
        if (self.right_eyelids_state == EyelidsState.CLOSED):
            lcd.message(self.right_eyelids_state.value)
        else:
            lcd.message(self.right_eye_state.value)
        
        # mouth
        lcd.setCursor(7, 1)
        lcd.message(self.mouth_state.value)

face = Face()

def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')

def set_up_lcd():
    # it might be possible to define custom characters
    # https://lastminuteengineers.com/arduino-1602-character-lcd-tutorial/
    turn_on_backlight()
    set_columns_lines()

def turn_on_backlight():
    mcp.output(3, 1)

def set_columns_lines():
    lcd.begin(16, 2)
  
def loop():
    set_up_lcd()

    while(True):         
        # lcd.clear() # causes flicker

        if random.random() > 0.95:
            face.blink()
        
        # if random.random() > 0.97:
        #     face.look_left()
        
        # if random.random() > 0.97:
        #     face.look_right()
         
        if random.random() > 0.93:
            face.look_forward()
        
        if random.random() > 0.93:
            face.smile()
        
        if random.random() > 0.95:
            face.do_not_smile()
        
        # if random.random() > 0.95:
        #     face.frown()
        
        # if random.random() > 0.97:
        #     face.wink()
        
        # if random.random() > 0.94:
        #     face.do_not_wink()
        
        face.display(lcd)
        face.update()
        sleep(0.2)
        
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
