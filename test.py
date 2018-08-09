import matplotlib.pyplot as plt
from numpy import linspace
import json
from utility import *
from simulation import *
config="plates2.json"
plates=loadPlateFile(config)
print("There are %s plates with radlen %.02e"%(len(plates),plates[0].radlen))
print("The Theta scatter rms is %.02e"%getScatterRMS(plates[0].radlen))
simulate(events=100000,plates=plates,plt=plt)
