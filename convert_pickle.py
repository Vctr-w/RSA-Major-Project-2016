import pickle
import sys

f = open(sys.argv[1])
a = pickle.load(f)

for i in range(10):
    print a[i]
