import matplotlib.pyplot as plt
from numpy import linspace
import json
from utility import *
from simulation import *

config="plates.json"
EVENTS=50000

rawPlates=None
def arrToPlate(plate):
    return Plate(plate['position'],getComposition(plate['composition']),False)

#print("There are %s plates with radlen %.02e"%(len(plates),plates[0].radlen))
#print("The Theta scatter rms is %.02e"%getScatterRMS(plates[0].radlen))

with open(config) as f:
    rawPlates=json.loads(f.read())

def getPositions(plates):
    pos=[]
    for plate in plates:
        if 'composition' in plate:
            pos.append(plate['position'])
    return pos

def setThickness(thick,plates):
    for plate in plates:
        if 'composition' in plate:
            plate['composition'][0][1]=thick
    return compPlates(plates)

def testPlates(thickness,plates):
    print("\nLooking at position %.04f"%thickness)
    resolutions=[]
    positions=getPositions(plates)
    plates=setThickness(thickness,plates)
    results,_rms=simulate(Plate(0,0,True),events=EVENTS,plates=plates)

    allPositions=results[0].positions
    
    real=[]
    reconstructed=[]
    toggle=(None,None)
    for res in results:
        real.append(res.realTrack)
        reconstructed.append(res.measurement)
        
    residuals=[]
    rms=[[] for i in positions]
    fitPos=allPositions[:3]+allPositions[-3:]
    #fitPos=allPositions[-3:]
    for reconTrack,realTrack in zip(reconstructed,real):
        #reconTrack needs to be only the ones that will be in the line of best fit.
        #fitPos needs to be the allPositions that will be in the line of best fit.
        newReconTrack=reconTrack[:3]+reconTrack[-3:]
        #newReconTrack=reconTrack[-3:]
        residuals.append(getManyResiduals(allPositions,fitPos,newReconTrack,realTrack,positions))
        
    for i,pos in enumerate(positions):
        rms[i].append(getRMS([res[i] for res in residuals]))
            
        print("\rsim done.")
    return rms

y=[testPlates(thick,rawPlates) for thick in linspace(.003,.005,10)]
x=getPositions(rawPlates)
with open("test.json", 'w+') as f:
    f.write(json.dumps({'y': y, 'x': x}))

for _y,label in zip(y,linspace(.003,.005,10)):
    plt.plot(x,_y,marker='8', label="%.04f"%label)
plt.legend(loc='top left')
plt.title("Stuff")
plt.xlabel("Positions")
plt.ylabel("rms of plates")
plt.show()
