#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pigpio
import RPi.GPIO as GPIO
from time import sleep


SrPin = 18	# ALT0\18 = BOARD_12
PIG = pigpio.pi()

def setup():
	###  Motor setup
	PIG.set_mode(18, pigpio.ALT0)    # ALT0_pin 18 = BOARD_pin 12
	PIG.write(18,0)

def destroy():
	### PIGPIO CleanUP
	PIG.set_mode(18, pigpio.INPUT)
	PIG.stop()

def loop():
	PIG.hardware_PWM(18, 50,1500/20000.0 *1000000)
	sleep(2)

if __name__ == '__main__':                      # Program start from here
        setup()
        try:
		loop()
        except KeyboardInterrupt:
		destroy()
