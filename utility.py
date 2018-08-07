from numpy.polynomial.polynomial import polyfit
import json
from math import *
from operator import itemgetter, attrgetter

class Plate:
    def __init__(self, position,radlength,isScoringPlane=False):
        self.pos=position
        self.position=position
        self.radlen=radlength
        self.radlength=radlength
        self.isScoringPlane=isScoringPlane
        

def cmToRad(input):
    return input/9.370 #Silicon had rad length of 9.37cm

def transform_to_origin(input):
    minimum=min(input)
    return [i-minimum for i in input]

def loadPlateFile(url):
    with open("plates.json") as f:
        plates=json.loads(f.read())
    return [Plate(plate['position'],plate['radlen'],False) for plate in plates]

def prepPlates(plates,scoringPlane):
    plates.append(scoringPlane)
    plates=sorted(plates, key=lambda ele: ele.pos)
    return plates

def getPlates(config,scoringPlane):
    plates=loadPlateFile(config)
    return prepPlates(plates,scoringPlane)


def plotLine(plotter, inputs, outputs):
    b,m=polyfit(inputs,outputs, 1)
    plotter.plot(inputs,[m*x+b for x in inputs])
    return b,m

def getTestPoint(x,y,testPoint,toggle,plt=None):
    b,m=polyfit(x[toggle[0]:toggle[1]],y[toggle[0]:toggle[1]],1)
    if plt is not None:
        plt.plot(x,[m*i+b for i in x])
    return m*testPoint+b

'''
a=sum 1
b=sum x
c=sum x^2
rms = sqrt((b/a)^2 - c/a)
'''
def getRMS(risiduals):
    a=len(risiduals)
    b=sum(risiduals)
    b=b*b
    c=sum([x*x for x in risiduals])/a
    return sqrt(c - (b/a)**2)

#currently going to assume, 3 plates on the left, 3 on the right with a sensor in the middle.
def getAdvancedRMS(results, plates, scoringPlane):
    mid=int(len(plates)/2)
    left=plates[:mid]
    right=plates[mid:]

    #Calculating risiduals uses the functions:
    # - getTestPoint(x,y,testPoint,toggle,plt=None)
    # - getRisidual( x, measured_tracks, testPoint, toggle, real_tracks )
    #Recalculate the risiduals by using getTestPoint with custom toggle
    #Then the same with getRisidual

    leftRisiduals=[getRisidual(result) for result in results]
    rightRisiduals=None
    # //
    
    leftSigma=getRMS(leftRisiduals)
    rightRigma=getRMS(rightRisiduals)
    
    return
    


def getRisidual( x, measured_tracks, testPoint, toggle, real_tracks ):
    b,m=polyfit(x[toggle[0]:toggle[1]],measured_tracks[toggle[0]:toggle[1]], 1)
    pred_y=m*testPoint+b
    for point,real_y in zip(x,real_tracks):
        if point==testPoint:
            return real_y-pred_y
    raise Exception("The test point given to calculate the risidual was not specified in either the config file or the scoring plane.\n%s:%s"%(testPoint, x))

# Plotting for json formatted like:
# [ [x_0,y_0],[x_1,y_1],...,[x_n,y_n] ]
def generalPloting(file_name, title, xlabel,ylabel,plt):
    data=None
    with open(file_name) as f:
        data=json.loads(f.read())
    x=[datum[0] for datum in data]
    y=[datum[1] for datum in data]
    plt.plot(x,y, linestyle="None", marker="o")
    b,m=plotLine(plt,x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def getComposition(materials):
    #materials should be an array with 2-tuples, (material, thickness)
    radlen=0
    for material in materials:
        radlen+=getRadlen(material[0],material[1])
    return radlen
    
KAPTON=28.6  #cm
SILICON=9.37 #cm
def getRadlen(thickness, material):
    material=material.lower()
    if material == "kapton":
        return thickness/KAPTON
    elif material == "silicon":
        return thickness/SILICON
    else:
        return None
