#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pigpio
import RPi.GPIO as GPIO
from time import sleep


TxPin = 15      # BOARD_15
RxPin = 16      # BOARD_16
SrPin = 18	# ALT0\18 = BOARD_12
PIG = pigpio.pi()

def setup():
 	###  Laser setup
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TxPin, GPIO.OUT)
        GPIO.setup(RxPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(TxPin, GPIO.HIGH)           # Set pin to high(+3.3V) to offthe laser
	###  Motor setup
	PIG.set_mode(18, pigpio.ALT0)    # ALT0_pin 18 = BOARD_pin 12
	PIG.write(18,0)

def destroy():
	### GPIO CleanUP
        GPIO.output(TxPin, GPIO.HIGH)           # led off
        GPIO.cleanup()                          # Release resource
	### PIGPIO CleanUP
	PIG.set_mode(18, pigpio.INPUT)
	PIG.stop()

def loop():
        GPIO.output(TxPin, GPIO.HIGH)  # Laser on

	PIG.hardware_PWM(18, 50,1500/20000.0 *1000000)
	sleep(2)
	for j in range(1,40):
		PIG.hardware_PWM(18, 50,1000/20000.0 *1000000)
		sleep(1)
		PIG.hardware_PWM(18, 50,2000/20000.0 *1000000)
		sleep(1)
	PIG.hardware_PWM(18, 50,1500/20000.0 *1000000)
	sleep(2)


if __name__ == '__main__':                      # Program start from here
        setup()
        try:
		loop()
        except KeyboardInterrupt:
		destroy()
