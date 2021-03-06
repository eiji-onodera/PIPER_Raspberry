import csv
from collections import defaultdict


class  brix():
	brix_data=defaultdict(int)

	def __init__(self,filepath):
		csv_header = ['degree','brix']
		with open(filepath, 'r') as f:
			for row in csv.DictReader(f, csv_header):
				self.brix_data[ int(row['degree']) ] = float(row['brix'] )

	def degree2brix(self,degree):
		ret = self.brix_data[int(degree)]
		# print("Degree: %d brix: %d %s" %(degree, self.brix_data[degree], degree in self.brix_data ) )  ← たまにバグる
		print("Degree: %d brix: %d %s" %(int(degree), ret , int(degree) in self.brix_data ) )

		if( int(degree) in self.brix_data ):
			return(ret)
		else:
			return(-1)

if __name__ == '__main__':                      # Program start from here
		bclass=brix('data.csv')
		print(bclass.degree2brix(1443))