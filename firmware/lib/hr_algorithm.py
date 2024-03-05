# Micropython version of SparkFun_MAX3010x_Sensor_Library
# Taken from https://github.com/kandizzy/esp32-micropython/blob/master/PPG/ppg/heartbeat.py

import time

HR_AVERAGE_SAMPLES = 16 

class HeartBeat(object):
    
    def __init__(self):
        self.IR_AC_Max = 20
        self.IR_AC_Min = -20

        self.IR_AC_Signal_Current = 0
        self.IR_AC_Signal_Previous = 0
        self.IR_AC_Signal_min = 0
        self.IR_AC_Signal_max = 0
        self.IR_Average_Estimated = 0

        self.positiveEdge = 0
        self.negativeEdge = 0
        self.ir_avg_reg = 0

        self.cbuf = [0] * 32
        self.offset = 0

        self.FIRCoeffs = [172, 321, 579, 927, 1360, 1858, 2390, 2916, 3391, 3768, 4012, 4096]

    def averageDCEstimator(self, wp, x):
        wp += ( ( ( x << 15) - wp) >> 4)
        self.ir_avg_reg = wp
        return (wp >> 15)

    def mul16(self, x, y):
        return(x * y)

    def lowPassFIRFilter(self, din):
        self.cbuf[self.offset] = din

        z = self.mul16(self.FIRCoeffs[11], self.cbuf[(self.offset - 11) & 0x1F])
      
        for i in range(11):
            z += self.mul16(self.FIRCoeffs[i], self.cbuf[(self.offset - i) & 0x1F] + self.cbuf[(self.offset - 22 + i) & 0x1F])

        self.offset += 1
        self.offset %= 32 #Wrap condition

        return(int(z >> 15))

    def checkForBeat(self, sample):
        beatDetected = False

        #  Save current state
        self.IR_AC_Signal_Previous = self.IR_AC_Signal_Current

        #  Process next data sample
        self.IR_Average_Estimated = self.averageDCEstimator(self.ir_avg_reg, sample)
        self.IR_AC_Signal_Current = sample - self.IR_Average_Estimated #self.lowPassFIRFilter(sample - self.IR_Average_Estimated)

        #print("prev: " + str(self.IR_AC_Signal_Previous) + "\ncurr: " + str(self.IR_AC_Signal_Current))
        #  Detect positive zero crossing (rising edge)
        if ((self.IR_AC_Signal_Previous < 0) and (self.IR_AC_Signal_Current >= 0)):
            self.IR_AC_Max = self.IR_AC_Signal_max
            self.IR_AC_Min = self.IR_AC_Signal_min

            self.positiveEdge = 1
            self.negativeEdge = 0
            self.IR_AC_Signal_max = 0

            #if ((IR_AC_Max - IR_AC_Min) > 100 & (IR_AC_Max - IR_AC_Min) < 1000)
            if ((self.IR_AC_Max - self.IR_AC_Min) > 20 and (self.IR_AC_Max - self.IR_AC_Min) < 1000):
              beatDetected = True

        #  Detect negative zero crossing (falling edge)
        if ((self.IR_AC_Signal_Previous > 0) and (self.IR_AC_Signal_Current <= 0)):
            self.positiveEdge = 0
            self.negativeEdge = 1
            self.IR_AC_Signal_min = 0

        #  Find Maximum value in positive cycle
        if (self.positiveEdge and (self.IR_AC_Signal_Current > self.IR_AC_Signal_Previous)): 
            self.IR_AC_Signal_max = self.IR_AC_Signal_Current

        #  Find Minimum value in negative cycle
        if (self.negativeEdge and (self.IR_AC_Signal_Current < self.IR_AC_Signal_Previous)):
            self.IR_AC_Signal_min = self.IR_AC_Signal_Current
        
        return beatDetected
    
class DetectHeartbeat(object):
    def __init__(self):
        #Variables for getting a finger pulse
        self.l_threshold = 2000
        self.u_threshold = 100000

        self.lastBeat = 0
        self.beat = HeartBeat()
        self.beatsPerMinute = 0
        self.beatAvg = 0
        self.prev_beatAvg = 0
        self.rateSpot = 0
        self.delta = 0

        self.start_finger_time = 0
        self.end_finger_time = 0
        self.finger_on = False
            
        self.average_hr_buffer = []

    def detectHeartbeat(self, ir):
        if (ir > self.l_threshold and ir < self.u_threshold):
            if (self.finger_on == False):
                self.start_finger_time = time.ticks_ms()
                self.finger_on = True
                #print("Loading...")
            
            #We sensed a beat!
            if(self.beat.checkForBeat(ir)):
                #print("Beat\n")
                self.delta = time.ticks_ms() - self.lastBeat
                self.lastBeat = time.ticks_ms()

                self.beatsPerMinute = 60 / (self.delta / 1000.0)
                
                self.prev_beatAvg = self.beatAvg
                #print(self.delta)
                #print("Beats Per Minute:", self.beatsPerMinute)
                
                if(self.beatsPerMinute < 255 and self.beatsPerMinute > 20):
                    self.beatAvg = self.calculateAverageHR(self.beatsPerMinute)

                #else:
                    #print("Irregularly high or low heartrate")
                            
    def calculateAverageHR(self, hr):
        average_hr = 0

        # if list containing values for average calculation is full
        if (len(self.average_hr_buffer) == HR_AVERAGE_SAMPLES):

            # rotate the list
            for i in range(HR_AVERAGE_SAMPLES-1):
                self.average_hr_buffer[i] = self.average_hr_buffer[i+1]

            self.average_hr_buffer[HR_AVERAGE_SAMPLES-1] = hr

            # calculate the average SpO2 value
            for i in range(HR_AVERAGE_SAMPLES):
                average_hr += self.average_hr_buffer[i]

            return average_hr / HR_AVERAGE_SAMPLES

        # otherwise append the samples to the list until the list is full
        else:
            self.average_hr_buffer.append(hr)

            for i in range(len(self.average_hr_buffer)):
                average_hr += self.average_hr_buffer[i]

            return average_hr / len(self.average_hr_buffer)

    def getBeatAverage(self):
        return self.beatAvg