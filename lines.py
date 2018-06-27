import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json


def iterate(y=[0], counter=0, std=1):
    if counter is 0: return y
    return iterate( y+[normal(y[-1],std) ], counter-1 )

def getTrackerHits(plates, events):
    x=[i%plates for i in range(events*plates)]
    y=[]
    for i in range(events): y+=iterate( [0], plates-1 )
    return x,y

#`position` is the position of the sensor plate.
def getSensorHits(plates, events, position=4):
    vals=[]
    for i in range(events):
        x=range(plates)
        y=iterate(counter=plates-1)
        val.append(getVal(position,x,y))
    return vals

def getSimulationData(plates, events, position=4):
    vals=[]
    _x=[]
    _y=[]
    for i in range(events):
        x=range(plates)
        y=iterate(counter=plates-1)
        val.append(getVal(position,x,y))
        _x+=x
        _y+=y
    return vals, _x, _y

plates=9
events=1000
total=plates*events

vals=getSensorHits(plates,events)

#plt.plot(vals,marker='o', linestyle='None')
#plotLine(plt,x,y)
#plt.plot(x,y, marker='.', linestyle='None')
plt.show()

