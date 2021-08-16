#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import json
from datetime import datetime
from time import sleep

import mesure
import sonic
import mqtt
import color
import brix


mqclient = mqtt.aws_mqtt(host = 'a287p9vwxu3415-ats.iot.us-east-2.amazonaws.com',topic = 'iot/topic')
distance = sonic.measure_distance(11,13)
ring=mesure.measure_brix(16,18,18)
blood=color.red_sensor(0x2a)
d2b=brix.brix('data.csv')

try:
	mqclient.connect()
	while True:
		sleep(1)
		if(distance.switch):
			print("Fire!!")
			mqclient.updateStatus('Scaning')
			degree_data = ring.get_degree()			# 糖度計測開始
			brix_data=d2b.degree2brix(degree_data)
			if(brix_data < 2):
				signal_data='Green'
			else:
				signal_data='Yellow'

			if(blood.red_sense()):					# 血液検査開始
				signal_data='Red'
				print("red")		
			color_data = blood.data

			msg={}							# データ送信処理
			msg['signal'] = signal_data
			msg['brix'] = brix_data
			msg['color'] = color_data
			msg['timestamp'] = datetime.now().isoformat(timespec='seconds')
			messageJson = json.dumps(msg)
			mqclient.publish(messageJson)
			print('All sequence complete.')

			mqclient.updateStatus('Online')
			distance.reset()

except KeyboardInterrupt:
	del mesure.measure_brix
	distance.stop()
	GPIO.cleanup()
	sleep(1)