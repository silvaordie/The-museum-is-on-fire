from main import Problem
import itertools
import time 
import os
import glob

f = open("P3_1_8.txt")
p = Problem(f)
#print(filename)
t=time.time()
p.solve(True)
print("    Elimination: "+ str(time.time()-t))
t=time.time()
p.solve(False)
print("    Enumeration: "+ str(time.time()-t))

""" path = str(os.curdir)

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

P3_3_2    
    Elimination: 0.010967731475830078
    Enumeration: 0.1186833381652832
P3_1_4    
    Elimination: 0.046877145767211914
    Enumeration: 7.81533670425415
P5_1_2
    Elimination: 0.09028339385986328
    Enumeration: 11.33936882019043   
    
    
    """