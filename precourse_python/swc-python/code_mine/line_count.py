# line_count.py

# The wc command in UNIX is a command line utility for printing newline, word and byte counts for files. It can return the number of lines in a file, the number of characters in a file and the number of words in a file. It can also be combine with pipes for general counting operations.

import sys
from glob import glob

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

if __name__ == '__main__':
	main()