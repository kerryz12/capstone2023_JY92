import matplotlib.pyplot as plt
import numpy as np
import csv
import emd
sample_rate = 100*0.112

with open('RR_Raw_Data_sub.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

data_array = np.array(data, dtype=int)

print(data_array.shape)
#print(data_array)

time, ir, green, red = data_array[:, 0], data_array[:, 1], data_array[:, 2], data_array[:, 3]

# Visualise the time-series for analysis
plt.figure(figsize=(12, 4))
#plt.plot(green)
#plt.show()

x=red+green+ir

imf = emd.sift.sift(x)
print(imf.shape)
plt.plot(imf)

IP, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'hilbert')

# Define frequency range (low_freq, high_freq, nsteps, spacing)
freq_range = (0.1, 0.4, 8, 'log')
f, hht = emd.spectra.hilberthuang(IF, IA, freq_range, sum_time=False)

# Run a mask sift
#imf = emd.sift.mask_sift(x, max_imfs=5)

emd.plotting.plot_imfs(imf)
plt.show()



