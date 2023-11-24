import matplotlib as plt

f = open('output.txt', 'r')

data = f.readlines.splitlines()
time = []
heartrate = []
spo2 = []

for s in data:
    temp = s.split()
    time.append(temp[0])
    heartrate.append(temp[1])
    spo2.append(temp[2])

plt.plot(time, heartrate, label="Heartrate")
plt.plot(time, spo2, label="SpO2")
plt.xlabel('Time')
plt.legend()
plt.show()
