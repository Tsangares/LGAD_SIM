import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace
from numpy.polynomial.polynomial import polyfit
from numpy.random import normal
from math import *
from random import random
from utility import *
import sys, resource, json

data=None
with open("front_plates_10000events.json") as f:
    data=json.loads(f.read())

x=[datum[0] for datum in data]
y=[datum[1] for datum in data]
plt.plot(x,y, linestyle="None", marker="o")
b,m=plotLine(plt,x,y)
plt.title("Using Front 3 Plates at 10k Events Each")
plt.xlabel("Sensor Position")
plt.ylabel("RMS of Test Point in Line of Best Fits")
plt.show()

