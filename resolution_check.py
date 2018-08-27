import matplotlib
from numpy.polynomial.polynomial import polyfit
import simulation as sim
import matplotlib.pyplot as plt
from numpy import linspace
from utility import *
events=100000
scoringPlane=Plate(153,.00076,True)
plates=getPlates("miniplates.json",scoringPlane)
RMS=[]
yuzhan=.004295
RES=linspace(.004,.0055,15)
for res in RES:
    results,rms=sim.simulate(plates=plates,events=events,resolution=res,toggle=(0,3))
    RMS.append(rms)
    print('done with %.05f'%res)


plt.plot(RES,RMS,linestyle="None", marker="8")
b,m=polyfit(RES,RMS,1)
minimum=m*RES[0]+b
maximum=m*RES[-1]+b

plt.plot([RES[0],RES[-1]],[minimum,maximum],'c')
_y=(yuzhan-b)/m
print(_y)
plt.plot([RES[0],RES[-1]],[yuzhan,yuzhan],'r')
plt.plot([_y,_y],[min(RMS),max(RMS)*.97], 'r')
#plt.plot([]
plt.title("Finding Space-Point Resolution Through Monte Carlo")
plt.xlabel("Space-Point Resolution, $\delta_y$ (mm)")
plt.ylabel("RMS of Residuals (mm)")
plt.figtext(.15,.8,s="Space-Point Resolution at RMS=%.04e is %.04e"%(yuzhan,_y))
plt.show()
