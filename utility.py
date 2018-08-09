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
    with open(url) as f:
        plates=json.loads(f.read())
    output=[]
    for plate in plates:
        myPlate=None
        if 'radlen' in plate:
            myPlate=Plate(plate['position'],plate['radlen'],False)
        elif 'composition' in plate:
            myPlate=Plate(plate['position'],getComposition(plate['composition']),False)
        else:
            myPlate=Plate(plate['position'],0,False)            
        output.append(myPlate)
    return output

def prepPlates(plates,scoringPlane):
    output=[plate for plate in plates]
    output.append(scoringPlane)
    output=sorted(output, key=lambda ele: ele.pos)
    return output

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
    #if len(left)==len(right) and left != right: print("yay!")
    #Calculating risiduals uses the functions:
    # - getTestPoint(x,y,testPoint,toggle,plt=None)
    # - getRisidual( x, measured_tracks, testPoint, toggle, real_tracks )
    #Recalculate the risiduals by using getTestPoint with custom toggle
    #Then the same with getRisidual
    leftRisiduals=[]
    rightRisiduals=[]
    for result in results:
        leftToggle=(None,mid)
        rightToggle=(mid,None)
        left=getRisidual(result.positions,result.measurement,scoringPlane.position, leftToggle,result.realTrack)
        right=getRisidual(result.positions,result.measurement,scoringPlane.position, rightToggle,result.realTrack)
        leftRisiduals.append(left)
        rightRisiduals.append(right)

    # //
    leftSigma=getRMS(leftRisiduals)
    rightSigma=getRMS(rightRisiduals)
    return leftSigma, rightSigma
    


def getRisidual( x, measured_tracks, testPoint, toggle, real_tracks ):
    inx=x[toggle[0]:toggle[1]]
    iny=measured_tracks[toggle[0]:toggle[1]]
    #print(len(inx),len(iny))
    #    b,m=polyfit(inx,iny, 1)
    b,m=polyfit(x[toggle[0]:toggle[1]],measured_tracks[toggle[0]:toggle[1]], 1)
    pred_y=m*testPoint+b
    for point,real_y in zip(x,real_tracks):
        if point==testPoint:
            return real_y-pred_y
    raise Exception("The test point given to calculate the risidual was not specified in either the config file or the scoring plane.\n%s:%s"%(testPoint, x))

# Plotting for json formatted like:
# [ [x_0,y_0],[x_1,y_1],...,[x_n,y_n] ]
def generalPlotting(title, xlabel,ylabel,plt,file_name=None):
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
    #or just a tuple.
    if type(materials) is tuple:
        return getRadlen(materials[0],materials[1])
    radlen=0
    for material in materials:
        radlen+=getRadlen(material[0],material[1])
    return radlen
    
KAPTON=28.6  #cm
SILICON=9.37 #cm
def getRadlen(material,thickness):
    material=material.lower()
    if material == "kapton":
        return thickness/KAPTON
    elif material == "silicon":
        return thickness/SILICON
    else:
        return None
