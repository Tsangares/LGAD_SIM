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
    return getTrack( plates, y+[normal(y[-1],abs(plates[counter]['thickness'])) ], counter-1 )

def getSimulationData(plates, events, position=470, plt=None):
    positions=[ plate['position'] for plate in plates ]
    x=[]
    for i in range(events): x+=positions.copy()
    y=[]
    vals=[]
    for i in range(events):
        track=getTrack(plates)
        vals.append(getVal(position,positions,track,plt))
        y+=track
    return vals, x, y

def getNuc(beta,mom,thickness,pos):
    c=3.0*10**6
    return (13.6)/(beta*c*mom)*pos*sqrt(thickness)*(1+.088*log(thickness))

def getMeasurement(y,std):
    return normal(y,std)

#(thickness,position)
plates=None
with open("plates.json") as f:
    plates=json.loads(f.read())
    
events=1000

sensor=470
plt.subplot(122)
vals,x,y=getSimulationData(plates,events, sensor)

plt.subplot(121)

plt.hist(vals,linspace(min(vals),max(vals),300))

plt.subplot(122)
plt.plot(x,y, marker='.', linestyle='None')
plt.plot([sensor,sensor], [min(y),max(y)])
plt.show()
