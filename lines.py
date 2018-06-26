import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from math import *
from random import random

def rand(x,ymin=0,ymax=1):
    return random()*(ymax-ymin)+ymin

def linespace(function,xmin=0,xmax=10,ymin=0,ymax=1, inputs=None):
    if inputs is None: yvar=range(xmin,xmax)
    return [function(x,ymin,ymax) for x in inputs]

def axies(x,y):
    return { 'y': y, 'x': x }

def plotLine(plotter, m, inputs, b):
    plotter.plot(inputs,[m*x+b for x in inputs])

def bruce(inputs=[-10,-9,-8,8,9,10],ymin=-1,ymax=1):
    xmin=min(inputs)
    xmax=min(inputs)
    outputs=linespace(rand,xmin,xmax,inputs=inputs)
    outputs[0]=0
    for i in inputs:
        plt.plot([i,i],[ymin,ymax], 'g')
    plt.plot(inputs, outputs, marker='o', linestyle='None')
    b,m=polyfit(inputs,outputs, 1)
    plotLine(plt, m, inputs, b)
    plt.title("Line of best fit y= %.3f x + %.3f"%(m,b))
    plt.show()


bruce()
