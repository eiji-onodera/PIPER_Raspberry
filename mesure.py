#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pigpio
import RPi.GPIO as GPIO
from time import sleep

class measure_brix:
	RxPin = 16      # BOARD_16
	SrPin = 18		# ALT0\18 = BOARD_12
	BasePin = 18
	PIG = None

	def __init__(self,val1,val2,val3):
		print("init called")
		self.RxPin = val1
		self.SrPin = val2
		self.BasePin = val3

		self.PIG = pigpio.pi()
		###  Motor setup
		self.PIG.set_mode(self.SrPin, pigpio.ALT0)    # ALT0_pin 18 = BOARD_pin 12
		#self.PIG.write(self.SrPin,0)

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		### Trainsiter setup (Laser Transimit)
		GPIO.setup(self.BasePin, GPIO.OUT)
		GPIO.output(self.BasePin, GPIO.HIGH)		#レーザー照射開始

		###  Laser Receiver setup
		GPIO.setwarnings(False)
		GPIO.setup(self.RxPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	def move(self,param):
		print("move to %s" % param )
		self.PIG.hardware_PWM(self.SrPin, 50, int( param/  20000.0 *1000000) )	#計測リング指定位置に移動		
		sleep(1)


	def get_degree(self):
		print("called")
		ave=0
		sum=0
		cnt=5
		for j in range(0,cnt):
			max=0
			min=2000
			self.PIG.hardware_PWM(self.SrPin, 50, int(1000/20000.0 *1000000) )	#計測リング開始位置に移動
			sleep(1)
			for i in range (1300,1600,5):
				degree=int( i/20000.0 *1000000)
				self.PIG.hardware_PWM(self.SrPin, 50, degree)
				if GPIO.input(self.RxPin) == GPIO.HIGH:
					if i < min:
						min=i
				sleep(0.05)
			sum+=min
			print("%d=%d ,ave=%d"  % (j,min,sum/(j+1))  )

		GPIO.output(self.BasePin, GPIO.LOW)		#レーザー照射停止
		self.PIG.hardware_PWM(self.SrPin, 50, int(700/20000.0 *1000000)	)		#計測リング停止位置に移動
		self.PIG.set_mode(self.SrPin, pigpio.INPUT)
		sleep(2)
		ave=sum/cnt
		print("average=%d ,at %d cnt "  % (ave,cnt)  )
		return(ave)

	def __del__(self):
		# Release resource
		### PIGPIO CleanUP		self.PIG.set_mode(18, pigpio.INPUT)
			self.PIG.stop()

def destroy():
	### GPIO CleanUP
        GPIO.cleanup()          

if __name__ == '__main__':                      # Program start from here
		ring=measure_brix(16,18,18)
		try:
			data = ring.get_degree()
			print("measured %d" %data)
			del measure_brix
			sleep(1)
			destroy()

		except KeyboardInterrupt:
			destroy()
