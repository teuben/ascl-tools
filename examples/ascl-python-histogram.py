#! /usr/bin/env python
#
#     figure made for ADASS0219 Vogelaar & Teuben BOF
#
import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd

# in ADS:   bibstem:"ascl.soft" AND full:"python"
# then go to Explore -> Citation Metrics

years = np.array( [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019] )
npy   = np.array( [3,    10,   20,   29,   48,   54,   60,   36,   64,   41]   )  # 43
nascl = np.array( [115,  227,  189,  181,  227,  207,  230,  195,  251,  176]  )  # 192
ratio = npy/nascl*100.0

print(ratio)

if True:
    plt.figure(1)
    plt.plot(years, nascl, 'C0o', alpha=0.5)
    plt.plot(years, npy,   'C1o', alpha=0.5)
    plt.step(years, nascl, where='mid')
    plt.step(years, npy,   where='mid')
    plt.plot(years, ratio)
    plt.savefig('python_in_ascl.png')
    plt.show()

if True:
    plt.figure(2)    
    # Values of each group
    bars1 = npy
    bars2 = nascl-npy
 
    # Heights of bars1 + bars2
    bars = np.add(bars1, bars2).tolist()
    
    # The position of the bars on the x-axis
    r = [0,1,2,3,4]
 
    # Names of group and bar width
    names = ['A','B','C','D','E']
    barWidth = 1
 
    # Create brown bars
    plt.bar(years, bars1,               color='#7f6d5f', edgecolor='white', width=barWidth)
    # Create green bars (middle), on top of the firs ones
    plt.bar(years, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=barWidth)

 
    # Custom X axis
    #plt.xticks(r, names, fontweight='bold')
    plt.title("Python codes in ASCL")
    plt.xlabel("year")
    plt.savefig('python_in_ascl.png')
 
    plt.show()
