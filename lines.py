import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json


def getTrack(plates, y=[0], counter=None):
    if counter is None: counter=len(plates)-1
    if counter is 0: return y
    return getTrack( plates, y+[normal(y[-1],plates[counter]) ], counter-1 )

def getSimulationData(plates, events, position=4):
    x=[i%len(plates) for i in range(events*len(plates))]
    y=[]
    vals=[]
    for i in range(events):
        track=getTrack(plates)
        vals.append(getVal(position,x[0:len(plates)],track))
        y+=track
    return vals, x, y

plates=[1,1,1,1,1,1,1,1,1]
events=10000

vals,x,y=getSimulationData(plates,events)

plt.subplot(121)

plt.hist(vals,linspace(-10,10,200))

plt.subplot(122)
plt.plot(x,y, marker='.', linestyle='None')

plt.show()
