import matplotlib.pyplot as plt
import matplotlib
from numpy import linspace
import json
import timeit
try:
    from simulation import simulate
    from utility import *
except Exception:
    from lgad.simulation import simulate
    from lgad.utility import *


'''

In this simulation we have a sensor that moves left to right.
We use this to test the properties of scattering and turning off plates.
'''

def humanLabel(label):
    left=label[0]
    right=label[1]
    if left is None:
        left="first"
    if right is None:
        right="last"
    return "Using plates %s to %s in the reconstruction."%(left,right)

def plotData(testRange,data,radlen,use,events):
    total=[]
    #Add error handling if the data is of the wrong format.
    matplotlib.rcParams.update({'font.size': 14, 'font.family': 'Ubuntu','axes.titlesize': 14})

    for datum,label in data:
        total+=(datum)
        plt.plot(testRange,datum,linestyle='None', marker='o', label=humanLabel(label))
    plt.xlabel("Scoring Plane Position (mm)")
    plt.ylabel("RMS of the Residuals (mm)")
    plt.ylim([0, max(total)*1.05])
    plt.legend()
    plt.grid(True, alpha=.2)
    coulomb=""
    if use is False: coulomb="No Coulomb"
    plt.title("Scoring Plane with radlength %.02f, %s %s Events"%(radlen,coulomb,events))

def batchSim(inputs,events,testRange,radlength,config):
    times=[]
    outputs=[]
    for use,toggle in inputs:
        start = timeit.default_timer()
        thisSim=[]
        for test in testRange:
            scoringPlane=Plate(test,radlength)
            plates=getPlates(config, scoringPlane)
            results,RMS=simulate(scoringPlane,events,plates,use=use,toggle=toggle)
            #RMS=getRMS(results
            thisSim.append(RMS)
        outputs.append(thisSim)
        stop = timeit.default_timer()
        times.append(stop-start)
        mean=sum(times)/len(times)
        timeLeft=mean*(len(inputs)-len(times))
        print("Finised sensor at %.04fmm in %.03f seconds with %.03f seconds left." %(test,(stop-start),timeLeft))
    print("Finished gathering data.")
    return outputs #Array of RMS values [float,float,...]

def prepareBatch(testRange, inputs, events, sensor_radlen,use,config):
    testRange=linspace(testRange[0],testRange[1],20)
    results=batchSim(inputs,events,testRange,sensor_radlen,config)
    if use is None:
        mid=int(len(results)/2)
        dataSet1=[(res,toggle[1]) for res,toggle in zip(results[:mid],inputs[:mid])]
        dataSet2=[(res,toggle[1]) for res,toggle in zip(results[-mid:],inputs[-mid:])]
        plt.subplot(121)
        plotData(testRange,dataSet1,sensor_radlen,inputs[0][0],events)
        plt.subplot(122)
        plotData(testRange,dataSet2,sensor_radlen,inputs[-1][0],events)
    else:
        data=[(res,toggle[1]) for res,toggle in zip(results,inputs)]
        plotData(testRange,data,sensor_radlen,use,events)
        
    plt.show()
    
    
def moving_one_plate(plate_min=305, plate_max=635, events=300, sensor_radlen=0.0,verbose=True, write_to_file=False,use=None,config="plates.json", toggle=None):
    if use is None:
        inputs=[(True,toggle),(False,toggle)]
    else:
        inputs=[(use,toggle)]
    prepareBatch((plate_min,plate_max),inputs,events,sensor_radlen,use,config)
    
def moving_plates(plate_min=305, plate_max=635, events=300, sensor_radlen=0.0,verbose=True, write_to_file=False,use=None,config="plates.json"):
    plates=loadPlateFile(config)
    mid=int(len(plates)/2)
    size=len(plates)
    if use is None:
        inputs=[
            (True,(None,mid)), (True,(1,3)), (True,(None,None)),
            (False,(None,mid)),(False,(1,3)),(False,(None,None)),
        ]
    else:
        inputs=[(use,(None,mid)),(use,(1,3)),(use,(None,None))]
    prepareBatch((plate_min,plate_max),inputs,events,sensor_radlen,use,config)

