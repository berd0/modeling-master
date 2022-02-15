#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 16:44:15 2022

@author: tom verguts
bayes optimization of the example described by Smith et al, 2021, PsychRxiv
illustrates how the log joint density can be used to optimize both Z and the parameters
see MCP book, figure 11.3b and accompanying text
"""

import numpy as np
import matplotlib.pyplot as plt

p_conc  = 0.9
prior_d = np.array([p_conc, 1-p_conc]) # z = 0, 1; should sum to 1
lik     = np.array([0.8, 0.2])   # prob x = 0 for z = 0, 1
z_label = ["concave", "convex"]  
x_label = ["shadow", "light"]

def logjoint(x, z, lik, priorz):
    """used for optimizing both z and lik"""
    return np.log(lik[z])*(1-x) + np.log(1-lik[z])*x + np.log(priorz)

def optimize_z(x, lik, priorz):
    return np.argmax(np.array([logjoint(x, 0, lik, priorz), logjoint(x, 1, lik, 1-priorz)]))

def optimize_lik(x, z):
    """optimize toward lik (first element only); maximum can be found explicitly but it's
	also based on the log joint function defined above"""
    return np.sum((1-x)*(1-z))/np.sum(1-z)

def free_energy(x, Q_p, prior):
	return Q_p*np.log(Q_p) + (1-Q_p)*np.log(1-Q_p) - Q_p*logjoint(x, 0, lik, prior) - (1-Q_p)*logjoint(x, 1, lik, 1-prior)

def surprise(x, prior):
    return -np.log(np.exp(logjoint(x, 0, lik, prior)) + np.exp(logjoint(x, 1, lik, 1-prior)))
	   
# optimize toward Z
observation = "light"
x  = x_label.index(observation)
print("i think the truth is {}!".format(z_label[optimize_z(x, lik, p_conc)]))

# optimize toward parameter lik
z = np.array([z_label.index("concave")]*4) # the truth is always concave
x = [x_label.index("shadow"), x_label.index("light"), x_label.index("shadow"), x_label.index("shadow")] # observations are usually shady
x = np.array(x)
print("my estimate of prob(shadow/concave) equals {}".format(optimize_lik(x, z)))

# calculate free energy
Q_p = 0.5 # probability of concave in Q(Z)
observation = "shadow"
x  = x_label.index(observation)
print("free energy = {:.2f}".format(free_energy(x, Q_p, p_conc)))
print("surprise = {:.2f}".format(surprise(x, p_conc)))

# plot free energy and surprise
fig, ax = plt.subplots(1, 2)

# calculate free energy across different priors on Z
low_z, high_z, step_size = 0.1, 0.9, 0.01
z_vec = np.arange(low_z, high_z, step_size)
F = np.ndarray(z_vec.size)
s = np.ndarray(z_vec.size)
for idx, z in enumerate(z_vec):
    F[idx] = free_energy(x, Q_p, z)
    s[idx] = surprise(x, z)

ax[0].plot(z_vec, F, color = "black")
ax[0].plot(z_vec, s, color = "red")

# calculate free energy across different Q's
q_vec = np.arange(low_z, high_z, step_size)
F = np.ndarray(q_vec.size)
s = np.ndarray(q_vec.size)
prior_z = 0.5 # probability of concave in P(Z)
for idx, q in enumerate(q_vec):
    F[idx] = free_energy(x, q, prior_z)
    s[idx] = surprise(x, z)

ax[1].plot(z_vec, F, color = "black")
ax[1].plot(z_vec, s, color = "red")




