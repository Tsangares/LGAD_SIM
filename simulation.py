
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
from multiprocessing import Pool as ThreadPool
#from multiprocessing.dummy import Pool as ThreadPool 
from itertools import repeat
import sys, resource, json
import timeit
#7.6*10**-4
'''
Run the simulation with a .1 radiation length for the scoring plane.
'''

THCK=THICKNESS=.00076
BE=BEAMENERGY=12500 #12.5GeV
'''
| Notes on Radiation Thickness

From arXiv:1603.09669v2,
the plates are:
 5.5e-3cm Silicon; radlen 9.37cm
 5.0e-3cm Kapton;  radlen 28.6cm
Plates are .0055/9.37 + 0.0050/28.6 = 7.6x10^-4 radlen
'''


'''

Set resolution to zero, the RMS should grow by sqrt(2)*rms(plate1);
'''
def getScatterRMS(thickness,velocity=BE):
    v=velocity
    out=(13.6)/(v) * sqrt(thickness) * (1+.088*log(thickness))
    return out

def getScatterAngle(thickness, use=True):
    if use is False: return 0
    rms=getScatterRMS(thickness)
    theta=normal(0,rms)
    return theta
    
def getPosition(positions,radlens, use=True):
    track=[]
    theta=0
    previous_x=0
    y=0
    for x,radlen in zip(positions,radlens):
        d=x-previous_x
        y+=d*tan(theta)
        track.append(y)
        theta+=getScatterAngle(radlen, use)
        previous_x=x
    return track

def getMeasurement(real_track, resolution):
    return [ normal(y,res) for y,res in zip(real_track,resolution) ] 

def tick(pos, radlens, use, res, sensor, toggle):
    real=getPosition(pos,radlens,use)
    measured=getMeasurement(real,res)
    val=getTestPoint(measured,pos,sensor,toggle)
    risidual=getRisidual(pos,real,measured,sensor,toggle)
    return real,measured,val,risidual
    

def getSimulationData(plates, events=1, sensor=470, plt=None, toggle=None, use=True, threads=8, verbose=True):
    start = timeit.default_timer()

    if toggle is None: toggle=(0,len(plates))
    positions=[ plate['position'] for plate in plates ]
    radlens=[ plate['radlen'] for plate in plates ]
    res=[ plate['resolution'] for plate in plates ]
    pos=[positions for i in range(events)]
    
    with ThreadPool(threads) as pool:
        results=pool.starmap(tick,zip(pos,repeat(radlens),repeat(use),repeat(res),repeat(sensor),repeat(toggle)))
        
    stop = timeit.default_timer()
    if verbose: print("Completed %s events in %.04f secconds"%(events,stop-start))
    
    return [datum[3] for datum in results]
#    return vals, pos, real_tracks, measured_tracks, risiduals

def simulate(events, sensor=470, config="plates.json", res=.0051826, plt=None, toggle=None, title=None, use=True):
    plates=loadPlateFile(config)
    risiduals = getSimulationData( plates, events, sensor, toggle=toggle, use=use)
    return getRMS(risiduals)

    

