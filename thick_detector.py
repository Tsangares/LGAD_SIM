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
        scoringPlane=Plate(test,0.1)
        plates=prepPlates(platesBasis, scoringPlane)
        
        start = timeit.default_timer()
        results,rms=simulate(scoringPlane,plates=plates,events=events,toggle=toggle, use=use)        
        newRMS=getAdvancedRMS(results,platesBasis,scoringPlane)
        normal.append(rms)
        advanced.append(newRMS)
        
        stop = timeit.default_timer()
        times.append(stop-start)
        mean=sum(times)/len(times)
        timeLeft=mean*(len(test_range)-len(times))
        print("Finised sensor at %.04fmm in %.03f seconds with %.03f seconds left." %(test,(stop-start),timeLeft))        
    print("Finished gathering data.")
    plt.subplot()
    plt.title("Averaging Left and Right Lines")
    plt.plot(test_range,normal,label="old reconstruction",linestyle="None",marker="8")
    plt.plot(test_range,advanced,label="new reconstruction",linestyle="None",marker="8")
    plt.legend(loc="top left")
    plt.show()
    
