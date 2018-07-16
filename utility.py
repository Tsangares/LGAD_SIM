from numpy.polynomial.polynomial import polyfit
import json
from math import *

def transform_to_origin(input):
    minimum=min(input)
    return [i-minimum for i in input]

def loadPlateFile(url):
    with open("plates.json") as f:
        plates=json.loads(f.read())
    return plates

def plotLine(plotter, inputs, outputs):
    b,m=polyfit(inputs,outputs, 1)
    plotter.plot(inputs,[m*x+b for x in inputs])
    return b,m

def getTestPoint(test_point,x,y,plt=None):
    b,m=polyfit(x,y, 1)
    if plt is not None: plt.plot(x,[m*i+b for i in x])
    return m*test_point+b

def getRMS(risiduals):
    return sqrt(sum([x*x for x in risiduals])/len(risiduals))

def getRisidual(x,y):
    b,m=polyfit(x,y, 1)
    test_point=m*x[1]+b
    return y[1]-test_point

