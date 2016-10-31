import pickle
import sys

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " [PICKLED FILE]")
    exit(1)

f = open(sys.argv[1])
a = pickle.load(f)

for i in range(10):
    print a[i]
