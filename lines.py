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
        vals.append(getVal(position,x,y))
    return vals

def getSimulationData(plates, events, position=4):
    vals=[]
    _x=[]
    _y=[]
    for i in range(events):
        x=range(plates)
        y=iterate(counter=plates-1)
        vals.append(getVal(position,x,y))
        _x+=x
        _y+=y
    return vals, _x, _y

plates=9
events=10000
total=plates*events

vals,x,y=getSimulationData(plates,events)
low=-10
high=10
bins=200
plt.subplot(121)
plt.hist(vals,[ i*(high-low)/bins+low for i in range(bins) ])
plt.subplot(122)
#plt.plot(vals,marker='o', linestyle='None')
#plotLine(plt,x,y)
plt.plot(x,y, marker='.', linestyle='None')
plt.show()

