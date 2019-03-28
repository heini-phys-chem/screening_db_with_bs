import sys,os
import numpy as np

lines = open(sys.argv[1], 'r').readlines()

data = {}

for i,line in enumerate(lines):
    inchi = (line[:-1].split()[-1])[1:-3]
    energy = (line[:-1].split()[1])[1:-2]

    data[inchi] = energy

for key, value in data.items():
    print(key, value)

