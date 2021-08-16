#! /usr/bin/python
import RPi.GPIO as GPIO
import time
import threading

class measure_distance:
	switch = False
	thread1 = None
	Loop_flag= False
	tpin = 0
	epin = 0

	status=0				# 0:距離が近い   1:距離が遠い
	near_threashold =0.1	# 遠近判定の閾値
	near_cnt =0
	far_cnt=0

	def __init__(self,val1,val2):
		self.tpin = val1 
		self.epin = val2
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.tpin,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(self.epin,GPIO.IN)
		time.sleep(2)
		self.thread1 = threading.Thread(target=self.measure_loop)
		self.start()
	
	def measure_loop(self):
		print(self.Loop_flag)
		while self.Loop_flag:
			GPIO.output(self.tpin, GPIO.HIGH)
			time.sleep(0.000015)
			GPIO.output(self.tpin, GPIO.LOW)
			while not GPIO.input(self.epin):
				pass
			t1 = time.time()
			while GPIO.input(self.epin):
				pass
			t2 = time.time()
			distance= (t2-t1)*340/2		

			if(distance < self.near_threashold) :			# 近い
				if(self.near_cnt <4):
					self.near_cnt +=1
				else:										# 4回以上連続で近距離判定だった場合
					if(self.status == 1):					#　　且つ、ステータスが遠距離 → 近距離と変化した場合
						self.switch=True					#		一度離れてから近づいたと判定し、スイッチをONにする
					self.status=0
				self.far_cnt=0
			else:											#遠い
				if(self.far_cnt <4):
					self.far_cnt +=1
				else:
					self.status=1
				self.near_cnt=0

			time.sleep(0.5)
			print('distance=%0.2f , status=%d ,far=%d ,near=%d' % (distance,self.status,self.far_cnt,self.near_cnt) )

	def start(self):
		self.Loop_flag= True
		self.thread1.start()

	def stop(self):
		self.Loop_flag= False
		time.sleep(0.5)

	def reset(self):
		self.switch=False

if __name__ == '__main__':
	try:
		d=measure_distance(11,13)

		while True:
			time.sleep(1)
			if(d.switch):
				print("Fire!!")
				d.reset()
	except KeyboardInterrupt:
		d.stop()
		GPIO.cleanup()





