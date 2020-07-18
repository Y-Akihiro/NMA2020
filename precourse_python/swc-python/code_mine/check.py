
# Write a program called check.py that takes the names of one or more inflammation data files as arguments and checks that all the files have the same number of rows and columns. What is the best way to test your program?

import sys
from glob import glob
import numpy as np

def main():
	script = sys.argv[0]
	filenames = sys.argv[1:]
	assert len(filenames) >= 1, 'Need to specify the files'


	if len(filenames) == 1:
		print('Only one file is checked.')
		data = np.loadtxt(filenames[0], delimiter=',')
		print('Data shape is ', data.shape)
	else:
		print(len(filenames), 'files are checked:')
		data_0 = np.loadtxt(filenames[0], delimiter=',')
		print(filenames[0])
		for i in filenames[1:]:
			print(i)
			data = np.loadtxt(i, delimiter=',')
			dt_shape = data.shape
			assert dt_shape != data_0, 'data structure is different'
		print('All files have', dt_shape[0],'rows and',dt_shape[1],'columns.')

	# filename = glob('../data/*.csv')
		
	#assert len()
	
	
	

if __name__ == '__main__':
	main()