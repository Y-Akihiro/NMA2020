# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 13:05:03 2020

@author: Akihiro Yamaguchi

Goals:
        * Plot the psychometric curve of previous response + correctness.
        * See/Check if there's any behavioral pattern that we can find.
"""
import os
import functions_get_ as fun
import numpy as np
import matplotlib.pyplot as plt

# Load data (run functions in 'main_behavior_analysis.py')
fname = [] # initialize the list
fname = fun.load_names()
print(fname)

srcdir = os.getcwd()
print('Current directory is...', srcdir)

# ====================== Lost Stuff ======================
alldat = np.array([])
for j in range(len(fname)):
    alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))

# =========== Get data for one selected session ===========
n_session = 11
dat, barea, NN, regions, brain_groups, nareas = fun.load_data(n_session, alldat)    
_, _, cont_diff, _, _, _ = fun.get_task_difference(n_session, dat)

# ====================== Compute Stuff ======================
# % rightward at each contrast difference for all trials (no history)
rightward = fun.get_rightward(dat, cont_diff) 

# check the contrast differences and the number of occurences
unique, counts = np.unique(cont_diff, return_counts=True) 
print('Contrast difference and no. of trials:')
for i,val in enumerate(unique): print(val, ':', counts[i])

# ==================== Analysis ====================

right_levels, n_trials = fun.get_correctness(dat, cont_diff)
import functions_plot_ as fun_plt

fun_plt.plot_correctness(dat, right_levels, cont_diff, n_trials, n_session, saveplot=False)

# Loop Over All the Sessions
for i in range(39):
    n_session = i
    dat, barea, NN, regions, brain_groups, nareas = fun.load_data(n_session, alldat)    
    _, _, cont_diff, _, _, _ = fun.get_task_difference(n_session, dat)   
    right_levels, n_trials = fun.get_correctness(dat, cont_diff)
    # fun_plt.plot_correctness(dat, right_levels, cont_diff, n_trials, n_session, saveplot=False)

