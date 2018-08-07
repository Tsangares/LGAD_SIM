import matplotlib.pyplot as plt
from numpy import linspace
import json
import timeit
try:
    from simulation import simulate
    from utility import *
    from moving_plates import *
except Exception:
    from lgad.simulation import simulate
    from lgad.utility import *
    from lgad.gnmoving_plates import *

    
def thick(plate_min=305, plate_max=635, events=300, sensor_radlen=0.0,verbose=True, write_to_file=False, toggle=None, use=None, config="plates.json"):
    test_range=linspace(plate_min,plate_max,20)
    normal=[]
    leftSigma=[]
    rightSigma=[]
    advanced=[]
    times=[]
    platesBasis=loadPlateFile(config)
    for test in test_range:
        scoringPlane=Plate(test,sensor_radlen)
        plates=prepPlates(platesBasis, scoringPlane)
        
        start = timeit.default_timer()
        
        normal.append(simulate(scoringPlane,plates=plates,events=events,toggle=toggle, use=use)[1])
        results,rms=simulate(scoringPlane,plates=plates,events=events,toggle=toggle, use=use)
        left,right=getAdvancedRMS(results,platesBasis,scoringPlane)
        leftSigma.append(left)
        rightSigma.append(right)
        
        stop = timeit.default_timer()
        times.append(stop-start)
        mean=sum(times)/len(times)
        timeLeft=mean*(len(test_range)-len(times))
        print("Finised sensor at %.04fmm in %.03f seconds with %.03f seconds left." %(test,(stop-start),timeLeft))        
    print("Finished gathering data.")
    plt.subplot()
    for l,r,pos in zip(leftSigma,rightSigma,test_range):
        print("left:right %.04f :%.04f :%.04f"%(l,r,pos))
    
    plt.plot(test_range,leftSigma,linestyle="None",marker='.')
    plt.plot(test_range,rightSigma,linestyle="None",marker='.')
    plt.show()
    
