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
with open("tmp.json") as f:
    data=json.loads(f.read())

x=[datum[0] for datum in data]
y=[datum[1] for datum in data]
plt.plot(x,y, linestyle="None", marker="o")
b,m=plotLine(plt,x,y)
plt.title("100k events Line of best fit y=%.04fx + %.04f"%(m,b))
plt.xlabel("Resolution")
plt.ylabel("Risidual")
plt.show()

