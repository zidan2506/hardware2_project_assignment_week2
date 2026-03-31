from filefifo import Filefifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
fifo = Filefifo(10, name = 'sinewave_250Hz_02.txt', repeat=False)


i2c = I2C(1,scl=Pin(15),sda=Pin(14), freq=400000)

w = 128
h = 64

oled = SSD1306_I2C(w,h,i2c)

prev = fifo.get()
curr = fifo.get()
sample_index = 1
sample_rate = 250
t1 = 2
t2 = 10
number_of_samples1 = t1*sample_rate
number_of_samples2 = t2*sample_rate
samples = []

y = 0

def scale(sample_value, max, min):
    scaled = ((sample_value-min)*100)/(max -min)
    return round(scaled)

while True:

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
    
    for n in range(number_of_samples2):
            
            data = fifo.get()
            if y > 56:
                oled.scroll(0,-8)
                y = 56
            oled.fill_rect(0,y,128,8,0)
            oled.text(f"{round(scale(data,max,min)):03d}",0,y)
            oled.hline(25, y, scale(data, max, min), 1)
            oled.show()
            y+=8
    oled.fill(0)
    oled.text("Done!", 40,32 )
    oled.show()
    break