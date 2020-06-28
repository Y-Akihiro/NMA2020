import sys
import numpy as np

def main():

	script = sys.argv[0]
	action = sys.argv[1]
	numbers = sys.argv[2:]
	assert action in ['add', 'subtract'], ('Action is not one of add or subtract' + action)
	
	if action == 'add':
		value = int(numbers[0]) + int(numbers[1])
	elif action == 'subtract':
		value = int(numbers[0]) - int(numbers[1])
	
	print(value)


if __name__ == '__main__':
	main()

