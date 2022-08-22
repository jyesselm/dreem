import pickle
import os, yaml
import pandas as pd

test_pickle = 'output/case_1/BitVector_Files/mutation_histos.p'
mhs = pickle.load(open(test_pickle, "rb"))

MAX_SIZE_A = 30

for m in mhs:
    print(m)
    for a in mhs[m].__dict__:
        print(a, (MAX_SIZE_A-len(a))*'-', mhs[m].__dict__[a])


    