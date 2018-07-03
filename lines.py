import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json

def getScatterAngle(pos,thickness=1,velocity=.999):
    v=velocity=.9+random()*.09
    while abs(v)>1: v=normal(1,.1)
    me=mass_electron=0.5109989461
    z=charge=1
    out=(13.6)/(v*v*me) *z* sqrt(thickness) * (1+.088*log(thickness))
    return out


def getPosition(positions,plates):
    out=[]
    theta=0
    last_x=0
    for x,plate in zip(positions,plates):
        dx=x-last_x
        out.append(dx*tan(theta))
        theta=getScatterAngle(x,plate['thickness'])
        last_x=x
    return out

def getMeasurement(real_track, plates, res=None):
    if res is None:
        return [ normal(y,plate['resolution']) for y,plate in zip(real_track, plates) ]
    else:
        return [ normal(y,1) for y in real_track ] 


def getSimulationData(plates, events=1, sensor=470, plt=None, res=None):
    positions=[ plate['position'] for plate in plates ]
    real_tracks=[]
    measured_tracks=[]
    vals=[]
    for e in range(events):
        start=e*len(plates)
        end=e*len(plates)+len(plates)
        real_tracks+=getPosition(positions, plates) # Start with a straight line
        measured_tracks+=getMeasurement(real_tracks[start:end],plates,res)
        vals.append(getVal(sensor,positions,measured_tracks[start:end]))

    x=[]
    for i in range(events): x+=positions.copy()
    
    return vals, x, real_tracks, measured_tracks


plates=None
with open("plates.json") as f:
    plates=json.loads(f.read())
    
events=1000 # Number of Events
sensor=470  # Sensor Position

# Run Simulation
vals, positions, real_track, measured_track = getSimulationData( plates, events, sensor )

plt.subplot(221)
plt.plot(positions, real_track, marker='.', linestyle='None')
plt.plot([sensor,sensor], [min(measured_track),max(measured_track)], 'r')
plt.title("Real Track")

plt.subplot(222)
plt.plot(positions, measured_track, marker='.', linestyle='None')
plt.plot([sensor,sensor], [min(measured_track),max(measured_track)], 'r')
plt.title("Measured Track")

plt.subplot(223)
plt.hist(vals,linspace(min(vals),max(vals),300))
#plt.title("Hits Line of Best Fit at x=%s"%sensor)

plt.subplot(224)
plt.axis("off")
plt.annotate(xy=(.3,.8),s="%s Events"%events)
plt.annotate(xy=(.3,.7),s="Sensor is at %smm"%sensor)

plt.show()


