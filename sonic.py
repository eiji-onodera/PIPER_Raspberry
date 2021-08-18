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

	status   : int=0				# 0:距離が近い   1:距離が遠い
	near_threashold: float=0.1		# 遠近判定の閾値
	near_cnt : int=0
	far_cnt  : int=0

	t1 : float=0
	t2 : float=0

	def __init__(self,val1,val2):
		self.tpin = val1 
		self.epin = val2
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.tpin,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(self.epin,GPIO.IN)
		time.sleep(2)

		self.thread1 = threading.Thread(target=self.measure_loop)
		self.thread2 = threading.Thread(target=self.self_recover)
		self.start()

	def self_recover(self):
		time.sleep(5)					#起動を遅延させる
		tmp_t1 : float=0
		tmp_t2 : float=0
		while self.Loop_flag:
			time.sleep(2)
#			print("t1 = %d %d  t2 %d %d flag=%s" %( tmp_t1, self.t1 , tmp_t2, self.t2, self.Loop_flag  ))  #debug用
			if(tmp_t1 == self.t1 and tmp_t2 == self.t2 and self.Loop_flag == True ):
				print("Recover Process start")
				self.near_cnt=0
				self.far_cnt=0
				GPIO.setup(self.epin,GPIO.OUT,initial=1)
				time.sleep(0.5)
				GPIO.setup(self.epin,GPIO.IN)
				time.sleep(0.5)

			tmp_t1=self.t1
			tmp_t2=self.t2

	def measure_loop(self):
		print(self.Loop_flag)
		while self.Loop_flag:
			GPIO.output(self.tpin, GPIO.HIGH)
			time.sleep(0.000015)
			GPIO.output(self.tpin, GPIO.LOW)
			while not GPIO.input(self.epin):
				pass
			self.t1 = time.time()
			while GPIO.input(self.epin):
				pass
			self.t2 = time.time()
			distance= (self.t2-self.t1)*340/2		

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
		self.thread2.start()

	def stop(self):
		self.Loop_flag= False
		time.sleep(0.5)

	def reset(self):
		self.switch=False

if __name__ == '__main__':
	try:
		d=measure_distance(11,13)

		while True:
			if(d.switch):
				print("Fire!!")
				d.reset()
	except KeyboardInterrupt:
		d.stop()
		GPIO.cleanup()





