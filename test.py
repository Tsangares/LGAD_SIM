import simulation as sim
import matplotlib.pyplot as plt
from numpy import linspace


x=linspace(0,1,10000)
y=[sim.getScatterRMS(rad) for rad in x]

plt.plot(x,y)
plt.show()


x=linspace(0,.01,10000)
y=[sim.getScatterRMS(rad) for rad in x]

plt.plot(x,y)
plt.show()


x=linspace(0,.001,10000)
y=[sim.getScatterRMS(rad) for rad in x]

plt.plot(x,y)
plt.show()

x=linspace(0,.0001,10000)
y=[sim.getScatterRMS(rad) for rad in x]

plt.plot(x,y)
plt.show()


x=linspace(0,.00001,10000)
y=[sim.getScatterRMS(rad) for rad in x]

plt.plot(x,y)
plt.show()
