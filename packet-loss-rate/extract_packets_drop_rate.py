#!/usr/bin/env python

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import brewer2mpl
from scipy.interpolate import spline
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

bmap = brewer2mpl.get_map('Set1', 'qualitative', 5)
colors = bmap.mpl_colors
mpl.rcParams['axes.color_cycle'] = colors


counts = 60

timeline = np.array(range(0, counts, 1))
timeline = timeline / float(8)

def extract_packet(filename):
    normalflowdown = []
    normalflowup = []
    normalflow = []
    fi = open(filename, 'r')
    countt = 0
    for line in fi.readlines():
        lines = line.split(' ')
        #print lines
        if lines[0] == 'rx_pkts_sec:' and int(lines[-1].split(',')[0]) != 0:
            #print lines[1].split(',')[0]
            normalflowdown.append(int(lines[-1]))
            normalflowup.append(int(lines[1].split(',')[0]))
            normalflow.append(float(normalflowup[countt])/float(normalflowdown[countt]))
            countt = countt + 1
            if countt == counts:
                break
    print counts        
    fi.close()
    return normalflow


#normalflow = extract_flow('normal.txt');
abnormalflow = extract_packet('master_abnormal.txt')
#stateless_normalflow = extract_flow('stateless_normal.txt')
stateless_abnormalflow = extract_packet('stateless_abnormal.txt')
baseline_abnormalflow = extract_packet('baseline_abnormal.txt')


print len(abnormalflow), len(stateless_abnormalflow), len(baseline_abnormalflow)

timeline_detail = np.linspace(timeline.min(), timeline.max(), counts)
#normalflow_detail = spline(timeline, normalflow, timeline_detail)
abnormalflow_detail = spline(timeline, abnormalflow, timeline_detail)
#stateless_normalflow_detail = spline(timeline, stateless_normalflow, timeline_detail)
stateless_abnormalflow_detail = spline(timeline, stateless_abnormalflow, timeline_detail)
baseline_abnormalflow_detail = spline(timeline, baseline_abnormalflow, timeline_detail)

xmajorLocator   = MultipleLocator(1)
xmajorFormatter = FormatStrFormatter('%1.0f')
xminorLocator   = MultipleLocator(0.5)
  
ymajorLocator   = MultipleLocator(10)
ymajorFormatter = FormatStrFormatter('%1.0f')
yminorLocator   = MultipleLocator(5)

plt.figure(figsize=(10,6.5))
ax = plt.subplot(111)

ax.xaxis.set_major_locator(xmajorLocator)  
ax.xaxis.set_major_formatter(xmajorFormatter)  
  
ax.yaxis.set_major_locator(ymajorLocator)  
ax.yaxis.set_major_formatter(ymajorFormatter)  
  
ax.xaxis.set_minor_locator(xminorLocator)  
ax.yaxis.set_minor_locator(yminorLocator)  
  
ax.xaxis.grid(True, which='major', ls='dotted')
ax.yaxis.grid(True, which='major', ls='dotted')

#plt.yscale('log')
plt.ylim(-5, 55)
plt.xlim(1, 7)
#plt.plot(timeline_detail, normalflow_detail, '-', label="Tripod", linewidth=1, marker='*')
plt.plot(timeline_detail, [(1-x)*100 for x in abnormalflow_detail], '-', label="Tripod", linewidth=3)#, marker='s')
#plt.plot(timeline_detail, stateless_normalflow_detail, '-', label="Stateless", linewidth=1, marker='^')
plt.plot(timeline_detail, [(1-x)*100 for x in baseline_abnormalflow_detail], '-', label="Baseline", linewidth=3)#, marker='o')
plt.plot(timeline_detail, [(1-x)*100 for x in stateless_abnormalflow_detail], '-', label="StatelessNF", linewidth=3)#, marker='o')

legend = plt.legend(loc='upper left', shadow=False, fontsize=20)

for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(20)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(20) 

plt.xlabel('Time(s)', fontsize=20)
plt.ylabel('Packet Loss Rate (%)', fontsize=20)

plt.savefig('packet_loss_rate.pdf')
plt.show()
