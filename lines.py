import json
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *


def iterate(y, counter):
    if counter is 1: return [y]
    return [y]+iterate( normal(y,1), counter-1 )

def sim(inputs):
    return iterate( 0, len(inputs) )
        
def process(x,y,counter=0):    
    if counter is 0: return y
    return process(x,y+sim(x),counter-1)

def init(plates, events):
    x=[i%plates for i in range(events*plates)]
    y=process(range(plates),[],counter=events)
    return x,y



plates=9
events=100
x,y=init(plates,events)

plt.plot(x,y, marker='.', linestyle='None')
plt.show()

#analize


#b,m=polyfit(inputs,outputs, 1)
#b,m=plotLine(plt, inputs, outputs)
#plt.title("Line of best fit y= %.3f x + %.3f"%(m,b))
