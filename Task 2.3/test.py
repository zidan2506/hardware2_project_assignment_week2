from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
fifo = Filefifo(10, name = 'sinewave_250Hz_03.txt', repeat=False)


i2c = I2C(1,scl=Pin(15),sda=Pin(14), freq=400000)

w = 128
h = 64

oled = SSD1306_I2C(w,h,i2c)

sample = fifo.get()
min_val = sample
max_val = sample 

sample_index = 1
sample_rate = 250
t1 = 2

number_of_samples1 = t1*sample_rate

y = 0



while True:


    if sw0.value() == 0:
        oled.fill(0)
        oled.text("Start!",35,25)
        oled.show()
        run = True
    if run:
        for n in range(number_of_samples1):
            try:
                next = fifo.get()
                if curr > prev and curr >= next:
                    print(f"Max = {curr}")
                    max = curr
                if curr <= prev and curr < next:
                    print(f"Min = {curr}")
                    min = curr
            except RuntimeError:
                break    
            prev = curr
            curr = next 

    for _ in range(number_of_samples1-1):
        
        sample = fifo.get()

        if sample < min_val:
            min_val = sample
        if sample > max_val:
            max_val = sample
        
    threshold = (min_val+max_val)/2
    fifo = Filefifo(10, name = 'sinewave_250Hz_03.txt', repeat=False)
    sample_index = 0
    edge_index = []

    prev = fifo.get()
    while True:
        try:
            curr = fifo.get()
            print("X")
            if prev < threshold and curr >= threshold:
                print("rising edge")
                edge_index.append(sample_index)
            prev =curr
            sample_index +=1
        except RuntimeError:
            break
    sum_freq = 0
    for n in range(len(edge_index)):
        
        if n+1 == len(edge_index):
            break

        period_samples = edge_index[n+1] - edge_index[n]
        freq = sample_rate/period_samples
        
        sum_freq+= freq

    avg_fred = sum_freq/ (len(edge_index)-1)
    #report
    print("Threshold: ", threshold)
    print("Estimated Frequency: ", round(avg_fred,2), "Hz")

    print("Rising edges detected at samples:")
    for n in edge_index:
        
        print(f"-{n}")
    print("Period: ")
    for n in range(len(edge_index)):

        if n+1 == len(edge_index):
            break
        period = edge_index[n+1]-edge_index[n]
        print(f"-{period} samples -> {round(period/sample_rate,2)} sec") 
    break