import glob

def main():
	pyfiles = glob.glob('*.py')
	print(pyfiles)


if __name__ == '__main__':
	main()