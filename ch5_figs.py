#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 10:25:17 2018

@author: tom
pics from chapter 5
"""
import numpy as np
import matplotlib.pyplot as plt

slope = [ -2, 0.5, 3]
intercept = [0, 1, 1]
low = -1
high = 2
font_size = 5

def conv(x, y, sign = 1, list = range(len(slope))):
    inside = True
    for i in list:
        if sign*(slope[i]*x + intercept[i] - y) > 0:
            inside = False
    return int(inside)

def plotlines():
    x = np.linspace(low, high)
    for i in range(len(slope)):
        y = slope[i]*x + intercept[i]
        plt.plot(x, y, color = "black")
    
# figure 5.2a
# determine the convex set
plt.subplot(121)
plotlines()
ngrid = 100
xi = np.linspace(low, high, ngrid)
# clunky vector operation in python :-(
extremes = [np.add(np.multiply(low,slope),intercept), np.add(np.multiply(high,slope),intercept)]
yi = np.linspace(np.amin(extremes), np.amax(extremes), ngrid)
Xi, Yi = np.meshgrid(xi, yi)
Zi = np.empty(Xi.shape)
# can the convex function be vectorized?
for row in range(len(xi)):
    for column in range(len(yi)):
        Zi[row,column] = conv(Xi[row,column],Yi[row,column])
plt.contourf(xi, yi, Zi)
plt.title("Fig 5.2a \nAn AND of linear functions is a convex set", {"fontsize": font_size})

# figure 5.2b
plt.subplot(122)
plotlines()
Zi_full = np.zeros(Xi.shape)
checklist = [[0], [2]]
for index in checklist:
    for row in range(len(xi)):
        for column in range(len(yi)):
            Zi[row,column] = conv(Xi[row,column],Yi[row,column],sign = -1, list = index)
    Zi_full = np.any([Zi_full,Zi],axis=0)        
plt.contourf(xi, yi, Zi_full)
plt.title("Fig 5.2b \nAn OR of convex sets", {"fontsize": font_size})