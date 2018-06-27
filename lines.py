import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource



def iterate(y, counter):
    if counter is 0: return y
    return iterate( y+[normal(y[-1],1) ], counter-1 )

def sim(inputs):
    return iterate( [0], len(inputs)-1 )
        
def process(x,y,counter=0):    
    if counter is 0: return y
    return process(x,y+sim(x),counter-1)

def init(plates, events):
    x=[i%plates for i in range(events*plates)]
    y=process(range(plates),[],counter=events)
    return x,y



plates=9
events=1000
#resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
#sys.setrecursionlimit=plates*events

x,y=init(plates,events)

plt.plot(x,y, marker='.', linestyle='None')
plt.show()

