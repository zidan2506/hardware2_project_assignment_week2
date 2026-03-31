from filefifo import Filefifo
import time
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

print(peak_index)
print(peak_values)

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