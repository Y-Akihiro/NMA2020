import sys
import numpy

def main():

	script = sys.argv[0]
#	assert len(sys.argv) == 4, 'Need 3 arguments: action + filename'
	if len(sys.argv) == 1: # no arguments, so print help message
		print("""Usage: python readings_08.py action filenames
		action must be one of --min --mean --max
		if filenames is blank, input is taken from stdin;
		otherwise, each filename in the list of arguments is processed in turn""")
		return
	
	action = sys.argv[1]
	filenames = sys.argv[2:]
	assert action in ['-n', '-m', '-x'], 'Action is not one of -n, -m, or -x: ' + action
	if len(filenames) == 0:
		process(sys.stdin, action)
	else:
		for filename in filenames:
			process(filename, action)

def process(filename, action):
    data = numpy.loadtxt(filename, delimiter=',')

    if action == '-n':
        values = numpy.min(data, axis=1)
    elif action == '-m':
        values = numpy.mean(data, axis=1)
    elif action == '-x':
        values = numpy.max(data, axis=1)

    for val in values:
        print(val)

if __name__ == '__main__':
   main()
