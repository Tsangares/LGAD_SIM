import matplotlib.pyplot as plt
from lines import simulate
from numpy import linspace
plate_min=305
plate_max=635
test_range=linspace(plate_min,plate_max,100)
outputs=[]
for test in test_range:
    outputs.append(simulate(events=10000,sensor=test,plt=None,toggle=(0,3)))
    print("At x=%s rms is %s"%(test, outputs[-1]))

plt.plot(test_range,outputs, linestyle='None')
plt.title("Position vs RMS")
plt.show()
