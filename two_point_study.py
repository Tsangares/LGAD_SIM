
import matplotlib
from numpy.polynomial.polynomial import polyfit
import simulation as sim
import matplotlib.pyplot as plt
from numpy import linspace
from utility import *
events=10000
rawPlates=loadPlateFile("plates.json")
RMS=[]
yuzhan=.004295
test_points=linspace(305,635,10)

def getTwoPoint(results,scoringPlane,s):
    positions=results[0].positions
    plate3=positions[1]
    plate2=positions[0]
    a=plate3-scoringPlane.pos
    d=plate3-plate2
    print(a)
    r=a/d
    S=s*sqrt(1+2*(r*r))
    print("S: %.05f"%S)
    return S

vals=[]

for test in test_points:
    scoringPlane=Plate(test,0.0,True)
    myPlates=prepPlates(rawPlates,scoringPlane)
    resolution=.00471
    results,rms=sim.simulate(plates=myPlates,events=events,toggle=(0,2),use=False)
    RMS.append(rms)
    print("RMS: %.05f"%rms)
    tp=getTwoPoint(results,scoringPlane,resolution)
    vals.append(tp)

    print('done with %.05f'%test)


plt.plot(test_points,RMS,linestyle="None", marker="8", label="Measure RMS from Residuals")
plt.plot(test_points,vals,linestyle="None", marker="o", label="Theoretical RMS from S=s*sqrt(1+2*r^2)")
plt.title("Theoretical S vs Measured RMS")
plt.xlabel("Position of the Scoring Plane (mm)")
plt.ylabel("RMS (mm)")
plt.legend()
plt.show()
