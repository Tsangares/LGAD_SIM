import matplotlib.pyplot as plt
from numpy import linspace
import json
from utility import *
from simulation import *

def arrToPlate(plate):
    return Plate(plate['position'],getComposition(plate['composition']),False)

#print("There are %s plates with radlen %.02e"%(len(plates),plates[0].radlen))
#print("The Theta scatter rms is %.02e"%getScatterRMS(plates[0].radlen))

def getPositions(plates):
    pos=[]
    for plate in plates:
        if 'variable' in plate and plate['variable'] is True:
            pos.append(plate['position'])
    return pos

'''
There is 2 scenarios:
 - Composition
 - Radlen
'''
def setThickness(thick,plates):
    for plate in plates:
        if 'variable' in plate and plate['variable'] is True:
            if 'composition' in plate:
                plate['composition'][0][1]=thick
            else:
                plate['radlen']=thick
    return compPlates(plates)

def testPlates(thickness,plates,events,left=True,right=True):
    print("\nLooking at position %.04f"%thickness)
    resolutions=[]
    positions=getPositions(plates)
    plates=setThickness(thickness,plates)
    results,_rms=simulate(Plate(0,0,True),events=events,plates=plates)

    allPositions=results[0].positions
    
    real=[]
    reconstructed=[]
    toggle=(None,None)
    for res in results:
        real.append(res.realTrack)
        reconstructed.append(res.measurement)
        
    residuals=[]
    rms=[[] for i in positions]
    fitPos=[]
    if left:
        fitPos+=allPositions[:3]
    if right:
        fitPos+=allPositions[-3:]
    #fitPos=allPositions[-3:]
    for reconTrack,realTrack in zip(reconstructed,real):
        #reconTrack needs to be only the ones that will be in the line of best fit.
        #fitPos needs to be the allPositions that will be in the line of best fit.
        newReconTrack=[]
        if left:
            newReconTrack+=reconTrack[:3]
        if right:
            newReconTrack+=reconTrack[-3:]
        #newReconTrack=reconTrack[-3:] #This is testing just the left plates
        residuals.append(getManyResiduals(allPositions,fitPos,newReconTrack,realTrack,positions))
        
    for i,pos in enumerate(positions):
        rms[i].append(getRMS([res[i] for res in residuals]))
        print("\rsim done.")
    return rms

#thicknesses
def variable_thickness(events=10000,config="eightPlates.json",sizes=[.00001,.0030,.0050,.0100,.0150,.1] ):
    rawPlates=None
    #sizes=linespace(.003,.005,10)
    with open(config) as f:
        rawPlates=json.loads(f.read())
    y=[testPlates(thick,rawPlates,events) for thick in sizes]
    x=getPositions(rawPlates)
    with open("test.json", 'w+') as f:
        f.write(json.dumps({'y': y, 'x': x}))
    for _y,label in zip(y,sizes):
        plt.plot(x,_y,marker='8', label="%.04f"%label)
    plt.legend(loc='upper left')
    plt.title("Stuff")
    plt.xlabel("Positions")
    plt.ylabel("rms of plates")
    plt.show()

def robustPloting(events=50000,config="eightPlates.json",sizes=[.00001,.0030,.0050,.0100,.0150,.02]):
    rawPlates=None
    #sizes=linespace(.003,.005,10)
    with open(config) as f:
        rawPlates=json.loads(f.read())
    allEight=[testPlates(thick,rawPlates,events) for thick in sizes]
    left=[testPlates(thick,rawPlates,events,right=False) for thick in sizes]
    right=[testPlates(thick,rawPlates,events,left=False) for thick in sizes]
    x=getPositions(rawPlates)

    plt.suptitle("Varying Thickness of Six Plates in Telescope's Gap", fontsize=16, style="italic")
    plt.subplot(2,1,1)
    for _y,label in zip(allEight[::-1],sizes[::-1]):
        plt.plot(x,_y,marker='8', label="%.04f"%label)

    plt.title("Using All Six Plates for Reconstruction")
    plt.ylabel("RMS of Residuals (mm)")

    plt.subplot(2,2,3)
    for _y,label in zip(left[::-1],sizes[::-1]):
        plt.plot(x,_y,marker='8', label="%.03f radlens"%label)
        
    plt.legend(loc='auto')
    plt.title("Using Left Three Plates")
    plt.ylabel("RMS of Residuals (mm)")
    plt.xlabel("Plate Positions (mm)")
    
    plt.subplot(2,2,4)
    for _y,label in zip(right[::-1],sizes[::-1]):
        plt.plot(x,_y,marker='8', label="%.03f"%label)
        plt.title("Using Right Three Plates")
    plt.xlabel("Plate Positions (mm)")
    plt.show()

robustPloting()
