import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json
#7.6*10**-4
THCK=THICKNESS=.00076
BE=BEAMENERGY=12500 #12.5GeV

def cmToRad(input):
    return input/9.370 #Silicon had rad length of 9.37cm

def getScatterRMS(thickness=THCK,velocity=BE):
    v=velocity
    thickness=cmToRad(thickness)
    out=(13.6)/(v) * sqrt(thickness) * (1+.088*log(thickness))
    return out

def getScatterAngle(thickness):
    rms=getScatterRMS()
    theta=normal(0,rms)
    return 0
    
def getPosition(positions,plates):
    out=[]
    theta=0
    last_x=0
    last_y=0
    for x,plate in zip(positions,plates):
        dx=x-last_x
        dy=dx*tan(theta)
        last_y+=dy
        out.append(last_y)
        theta=getScatterAngle(plate['thickness'])
        last_x=x
    #return [0 for i in plates]
    return out

def getMeasurement(real_track, plates, res=None):
    if res is None:
        return [ normal(y,plate['resolution']) for y,plate in zip(real_track, plates) ]
    else:
        return [ normal(y,res) for y in real_track ] 


def getSimulationData(plates, events=1, sensor=470, plt=None, res=None):
    positions=[ plate['position'] for plate in plates ]
    real_tracks=[]
    measured_tracks=[]
    vals=[]
    risiduals=[]
    for e in range(events):
        start=e*len(plates)
        end=e*len(plates)+len(plates)
        real_tracks+=getPosition(positions, plates) # Start with a straight line
        measured_tracks+=getMeasurement(real_tracks[start:end],plates,res)
        vals.append(getVal(sensor,positions[0:3],measured_tracks[start:end][0:3]))
        risiduals.append(getRisidual(positions[0:3],measured_tracks[start:end][0:3]))
    x=[]
    for i in range(events): x+=positions.copy()
    
    return vals, x, real_tracks, measured_tracks, risiduals

def getRMS(risiduals):
    return sqrt(sum([x*x for x in risiduals])/len(risiduals))

plates=None
with open("plates.json") as f:
    plates=json.loads(f.read())

print("No Theta")
events=100000 # Number of Events
sensor=470  # Sensor Position
# Run Simulation
goal_rms=.0042
last_rms=0.0
last_res=.0051826
for j in range(1):
    ress=[]
    for i in range(1):
        vals, positions, real_track, measured_track, risiduals = getSimulationData( plates, events, sensor, res=last_res)
        last_rms=getRMS(risiduals)
        ress.append(last_rms)
    print("With a resolution of %.06f we have an average risidual of %.06f" % (last_res,sum(ress)/len(ress)))
    last_res-=.00002

#plt.hist(ress, linspace(min(ress),max(ress),300))
#plt.show()
#print("Res %s gives us rms of %s"%(last_res,last_rms))

      
'''
plt.subplot(221)
plt.plot(positions, real_track, marker='.', linestyle='None')
plt.plot([sensor,sensor], [min(measured_track),max(measured_track)], 'r')
plt.title("Real Track")
plt.ylabel("Hit Location (mm)")

plt.subplot(222)
plt.plot(positions, measured_track,marker='.', linestyle='None')
plt.plot([sensor,sensor], [min(measured_track),max(measured_track)], 'r')
plt.title("Measured Track")
plt.xlabel("Plate Positions (mm)")



plt.subplot(223)
plt.hist(vals,linspace(min(vals),max(vals),300))
plt.xlabel("Veritle Axis, Hit Location (mm)")
plt.ylabel("Number of Hits (count)")
#plt.title("Hits Line of Best Fit at x=%s"%sensor)

plt.subplot(224)
#plt.axis("off")
#plt.annotate(xy=(.3,.8),s="%s Events"%events)
#plt.annotate(xy=(.3,.7),s="Sensor is at %smm"%sensor)
#plt.annotate(xy=(.3,.6),s="RMS of Measurement is 1std")
plt.hist(risiduals, linspace(min(risiduals),max(risiduals),300))
print("RMS of Risiduals = %s"%(  ))
plt.show()
'''


