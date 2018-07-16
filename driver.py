import matplotlib.pyplot as plt
from lines import simulate
from numpy import linspace
import json
plate_min=305
plate_max=635
test_range=linspace(plate_min,plate_max,20)

both_plates=[]
front_plates=[]
events=10000
for test in test_range:
    front_plates.append(simulate(events=events,sensor=test,plt=None,toggle=(0,3)))
    both_plates.append(simulate(events=events,sensor=test,plt=None,toggle=None))
    print("Finised sensor at %.04fmm." %test)

plt.plot(test_range,front_plates, linestyle='None', marker='o', label='Front Plates')
plt.plot(test_range,both_plates, linestyle='None', marker='o', label='All Plates')
plt.xlabel("Scoring Plane Position (mm)")
plt.ylabel("RMS of Test Point in Line of Best Fits")
plt.ylim([0, max(front_plates)*1.05])
plt.legend(loc='upper left')
plt.grid(True, alpha=.2)
plt.title("Moving Scoring Plane With %s Events"%events)
file_name="moving_sensor.json"
with open(file_name,"w+") as f:
    output={
        'test_range': test_range.tolist(),
        'both_plates': both_plates,
        'front_plates': front_plates
    }
    f.write(json.dumps(output))

print('wrote to file %s' % file_name)
plt.show()
