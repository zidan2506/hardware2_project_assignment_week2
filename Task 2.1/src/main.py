from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
from filefifo import Filefifo


i2c = I2C(1,scl=Pin(15),sda=Pin(14), freq=400000)

w = 128
h = 64

oled = SSD1306_I2C(w,h,i2c)

sw0 = Pin(9, Pin.IN, Pin.PULL_UP) #pressed => sw0.value()=0
sw1 = Pin(8, Pin.IN, Pin.PULL_UP) #pressed => sw0.value()=0
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)
x=10
y= 32

oled.text("Task 2.1", 25, 24)
oled.text("Press SW1", 25,32)
oled.show()

run = False

while True:


    if sw0.value() == 0:
        oled.fill(0)
        oled.text("Start!",35,25)
        oled.show()
        run = True

    if run:
        fifo = Filefifo(10, name = 'sinewave_250Hz_01.txt', repeat=False)

        prev = fifo.get()
        curr = fifo.get()

        sample_index = 1
        sample_rate = 250

        peak_index = []
        peak_values = []
        while True:
            
            try:
                next = fifo.get()
            except RuntimeError:
                break
            if curr > prev and curr >= next :
                peak_index.append(sample_index)
                peak_values.append(curr)
            
            sample_index += 1
            prev = curr
            curr = next



        interval_1 = peak_index[1] - peak_index[0]
        interval_2 = peak_index[2] - peak_index[1]
        interval_3 = peak_index[3] - peak_index[2]

        t1 = interval_1/sample_rate
        t2 = interval_2/sample_rate
        t3 = interval_3/sample_rate
        average_period = (t1+t2+t3)/3

        report = f"""
            Peak 1 at sample: {peak_index[0]}
            Peak 2 at sample: {peak_index[1]} 
            Peak 3 at sample: {peak_index[2]} 
            Peak 4 at sample: {peak_index[3]}

            Peak-to_Peak intervals:
            Interval 1: {interval_1}, {t1} seconds.
            Interval 2: {interval_2}, {t2} seconds.
            Interval 3: {interval_3}, {t3} seconds.

            Frequency = {1/average_period} Hz
        """
        print(report)
