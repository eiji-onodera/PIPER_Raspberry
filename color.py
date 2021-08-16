#!/usr/bin/python3
import smbus
import time

class red_sensor:
	bus=None
	addr=None
	data=None

	def __init__(self,val):
		self.bus = smbus.SMBus(1)
		self.addr = val


	def red_sense(self):
		self.bus.write_byte_data(self.addr , 0x0, 0xe4) #リセット
		self.bus.write_byte_data(self.addr , 0x1, 0x0c) #倍率
		self.bus.write_byte_data(self.addr , 0x2, 0x30) #倍率
		self.bus.write_byte_data(self.addr , 0x0, 0x84) #リセット、wakeup
		self.bus.write_byte_data(self.addr , 0x0, 0x04) #リセット解除
		time.sleep(3)
		data = self.bus.read_i2c_block_data(self.addr , 0x03, 8) #8バイトの読み出し
		R = data[0] *256 + data[1]
		G = data[2] *256 + data[3]
		B = data[4] *256 + data[5]
		Ir = data[6] *256 + data[7]
		TOT=R+G+B

		per_R=round(R/TOT*100)
		per_G=round(G/TOT*100)
		per_B=round(B/TOT*100)
		self.data='R%02dG%02dB%02d' % (per_R, per_G, per_B)+'＠S11059-02Dt'
		print( f"TOT={TOT}, R={R}% ,G={G}% ,B={B}% "+ self.data )
		if( per_R - per_G >= 8 and per_R - per_B >=8 ):		# R率が G率,　B率どちらより8% 以上高ければ赤と判定
			return(True)
		else:
			return(False)

if __name__ == '__main__':
	try:
		c=red_sensor(0x2a)
		if( c.red_sense()):
			print("red")
	except KeyboardInterrupt:
		del c









