#!/bin/python

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.colors as colors
from matplotlib import cm

'''
Code to read example post file created by SCICHEM and plot mean concentration contours over the whole period.
Contour scales can be Linear or Log based on value of isLinear. 
'''
isLinear = True

# Set the location of the source
src = np.array([-86.511795,28.044143]) 
print src

# Add column names form the SCICHEM post file
colNames = 'X             Y      AVECONC    ZELEV    ZHILL    ZFLAG    AVE     GRP       DATE'.split()
cwk = pd.read_table('conc_avg_168hr.plt',skiprows=8,sep=r'\s*',names=colNames) 
#print cwk.head()
#print cwk.tail()

# Group the post output by group for X and Y. To make a flat table use as_index set to false.
cwg = cwk.groupby(['X','Y'],as_index=False)
#print cwg.head()
#print cwg.tail()

# Calculate the mean average concentration over the whole period
cMean = cwg['AVECONC'].mean()
print cMean.head()
print cMean.tail()


# Set the X,Y and C values from the cMean values 

X = cMean['X'].values
#print 'X: ',cMean['X'].values
Y = cMean['Y'].values
#print 'Y: ',cMean['Y'].values
C = cMean['AVECONC'].values
#print 'C: ',cMean['AVECONC'].values

cMax = cMean['AVECONC'].max()

# Set contours levels based on linear or logscale
if isLinear:
    num   = 10 
    vmin  = 0.0
    vmax  = (int(cMax/num)+1)*num
    levels = np.linspace(vmin,vmax,num=num)
    lnorm  = colors.Normalize(levels,clip=False)
else:
    num  = 7
    vmax = int(np.log10(cMax)) + 1
    vmin = vmax - num + 1
    levels = np.logspace(vmin,vmax,num=num,base=10.0)
    lnorm  = colors.LogNorm(levels,clip=False)
clrmap = plt.cm.get_cmap('jet',len(levels)-1)
print levels

# Create contour lines using tri functions
triangles = tri.Triangulation(X, Y)
CS = plt.tricontour(X, Y, C, 15, norm = lnorm, levels=levels,linewidths=0.5, colors='k')

# Create filled contour and set color limits
if isLinear:
  CS = plt.tricontourf(X, Y, C, 15, norm= lnorm, levels=levels, cmap=clrmap, vmin=vmin)
  CS.set_clim(vmin,vmax)
else:
  CS = plt.tricontourf(X, Y, C, 15, norm= lnorm, levels=levels, cmap=clrmap, vmin=10.**vmin)
  CS.set_clim(10.**vmin,10.**vmax)

cbar = plt.colorbar(ticks=levels,format='%5.1e') # draw colorbar    

# Add source location to plot
plt.scatter(src[0],src[1],marker='*')

# Set title, labels and save plot
plt.title('Conc (ug/m3)')
plt.xlabel('Lon')
plt.ylabel('Lat')
plt.hold(False)
#plt.show()
plt.savefig('AvgCncContour.png')
