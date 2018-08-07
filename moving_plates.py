import matplotlib.pyplot as plt
from numpy import linspace
import json
import timeit
try:
    from simulation import simulate
    from utility import *
except Exception:
    from lgad.simulation import simulate
    from lgad.utility import *


def plotData(testRange,data,radlen,use,events):
    total=[]
    for datum,label in data:
        total+=(datum)
        plt.plot(testRange,datum,linestyle='None', marker='o', label=label)
    plt.xlabel("Scoring Plane Position (mm)")
    plt.ylabel("RMS of the Risiduals (mm)")
    plt.ylim([0, max(total)*1.05])
    plt.legend(loc='upper left')
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
            thisSim.append(RMS)
        outputs.append(thisSim)
        stop = timeit.default_timer()
        times.append(stop-start)
        mean=sum(times)/len(times)
        timeLeft=mean*(len(inputs)-len(times))
        print("Finised sensor at %.04fmm in %.03f seconds with %.03f seconds left." %(test,(stop-start),timeLeft))
    print("Finished gathering data.")
    return outputs

def prepareBatch(testRange, inputs, events, sensor_radlen,use,config):
    testRange=linspace(testRange[0],testRange[1],20)
    results=batchSim(inputs,events,testRange,sensor_radlen,config)
    if use is None:
        mid=int(len(results)/2)
        dataSet1=[(results[mid:],str(toggle))]
        dataSet2=[(results[:mid],str(toggle))]
        plt.subplot(121)
        plotData(testRange,[dataSet1],sensor_radlen,use,events)
        plt.subplot(122)
        plotData(testRange,[dataSet2],sensor_radlen,use,events)
    else:
        data=[(res,toggle[1]) for res,toggle in zip(results,inputs)]
        plotData(testRange,data,sensor_radlen,use,events)
        
    plt.show()
    
    
def moving_plate(plate_min=305, plate_max=635, events=300, sensor_radlen=0.0,verbose=True, write_to_file=False,use=None,config="plates.json"):
    if use is None:
        inputs=[(True,None),(False,None)]
    else:
        inputs=[(use,None)]
    prepareBatch((plate_min,plate_max),inputs,events,sensor_radlen,None,use,config,)
    
def moving_plates(plate_min=305, plate_max=635, events=300, sensor_radlen=0.0,verbose=True, write_to_file=False,use=None,config="plates.json"):
    if use is None:
        inputs=[
            (True,(0,3)), (True,(1,3)), (True,(0,11)),
            (False,(0,3)),(False,(1,3)),(False,(0,11)),
        ]
    else:
        inputs=[(use,(0,3)),(use,(1,3)),(use,(0,11))]
    prepareBatch((plate_min,plate_max),inputs,events,sensor_radlen,use,config)

