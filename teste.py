from main import Problem
import itertools
import time 
import os
import glob

path = str(os.curdir)

for filename in glob.glob(os.path.join(path, '*.txt')):
    f = open(filename)

    p = Problem(f)
    print(filename)
    t=time.time()
    p.solve(True)
    print("    Elimination: "+ str(time.time()-t))
    t=time.time()
    p.solve(False)
    print("    Enumeration: "+ str(time.time()-t))