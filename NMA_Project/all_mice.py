# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 09:25:25 2020

@author: Akihiro

Goal(s):
        * See if we can find any meaningful behavioral trend from the 
            39 sessions (10050 trials).
Steps: 
        i) Load Data (...Completed)
        ii) Sort Data by mice (...Completed)
        iii) Analyze: make psychometric curve (...Completed)
        iv) Analyze: psychometric curve of prev. response & difficulty (Completed)
        v) Analyze: bar plot (Completed))
"""

import os
import functions_get_ as fun
import numpy as np
# import matplotlib.pyplot as plt

# Load data (run functions in 'main_behavior_analysis.py')
fname = [] # initialize the list
fname = fun.load_names()
print(fname)

srcdir = os.getcwd()
print('Current directory is...', srcdir)

# ====================== i) Lost Stuff ======================
alldat = np.array([])
for j in range(len(fname)):
    alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))

# ====================== ii) Combine 39 session data ======================
dat_categ = ['contrast_left', 'contrast_right', 'response']
nans = np.empty([len(dat_categ),1])*np.nan
data_all = dict(zip(dat_categ, nans))
length = 0
for i in range(len(alldat)): # loop for each session
    print('session:', i, ' with length', len(alldat[i]['response']))        
    for categ in dat_categ:
        dat = alldat[i][categ]
        data_all[categ] = np.append(data_all[categ],dat)
        # dat = alldat[n_session]['response']
        # mice_data[(unique_names[i], 'response')] = dat
    
    length += len(alldat[i]['response'])

# Remove the first 'NaN'
for categ in dat_categ:
    data_all[categ] = data_all[categ][1:]

data_all['mouse_name'] = 'all'
    
# ====================== iii) Analyze & Plot Stuff ======================
cont_diff = data_all['contrast_left'] - data_all['contrast_right']
rightward = fun.get_rightward(data_all, cont_diff)

# ==== Psycometric curve of all trials ====
import functions_plot_ as fun_plt
fun_plt.plot_1psychometric(cont_diff, rightward, 10050, data_all)

# ==== Psycometric curve with previous response & task difficulty ====
idx_RL, right_levels = fun.get_right_history(data_all, cont_diff)
fun_plt.plot_psychometric(cont_diff, rightward, data_all['response'], right_levels,
                          idx_RL, 10050, data_all, srcdir)

# ==== Make a bar plot ====
langs, diff_mean, diff_std = fun.get_bars_data(right_levels)
fun_plt.plot_bars(langs, diff_mean, diff_std, srcdir, 10050)

# ==== Psycometric curve with previous response & correctness ====

import superstition_check as sc
idx_RL, right_levels, keys = sc.get_belief(data_all)
def plt_belief_all(idx_RL, right_levels, keys, 
                   cont_diff, rightward, srcdir,
                   saveplot=False):
    '''
    Input
    * idx_RL - indices of left/right choices
    * right_levels - % rightward
    * keys - keys of the dictionary: lc, lic, rc, ric, zc, zic
    * cont_diff - contrast difference (maybe not necessary?)
    * rightward - % rightward for 'all' case (not necessary?)

    * keys
    '''
    xdata = np.unique(cont_diff)
    ydata = rightward
    
    fig = plt.figure(figsize=(8,6))
       
    plt.plot(xdata, ydata,'ro-', label=keys[3]+'(%1.0f)'%len(idx_RL[3]), alpha=0.5, linewidth=3)
       
    plt.plot(xdata, right_levels[keys[6]],'D-',  color=colors['darkviolet'], 
             label=keys[6]+' (%1.0f)'%(idx_RL[6].size), linewidth=2)
    plt.plot(xdata, right_levels[keys[5]],'^:',  color=colors['violet'], 
    		 label=keys[5]+' (%1.0f)'%(idx_RL[5].size), linewidth=2)
    plt.plot(xdata, right_levels[keys[4]],'x--', color=colors['lime'], 
    		 label=keys[4]+' (%1.0f)'%(idx_RL[4].size), linewidth=2, alpha=0.5)
    plt.plot(xdata, right_levels[keys[2]],'x--', color=colors['deeppink'], 
    		 label=keys[2]+' (%1.0f)'%(idx_RL[2].size), linewidth=2, alpha=0.5)
    plt.plot(xdata, right_levels[keys[1]],'^:',  color=colors['skyblue'], 
    		 label=keys[1]+' (%1.0f)'%(idx_RL[1].size), linewidth=2)
    plt.plot(xdata, right_levels[keys[0]],'D-',  color=colors['dodgerblue'], 
    		 label=keys[0]+' (%1.0f)'%(idx_RL[0].size), linewidth=2)
    
    plt.xlabel('Contrast difference')
    plt.ylabel('Rightward (%)')
    plt.title('Mice: ' + name +' (superstition)', 
    		  fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    
    plt.grid(alpha=0.4)
    fig.show()

    if saveplot:
        print('Saving a figure to', srcdir)
        plt.savefig('belief_' + name + '.png')
        plt.close(fig)

plt_belief(data_all, n_session, cont_diff, rightward, srcdir,
           idx_RL, right_levels, keys, saveplot=False)



right_levels, n_trials = fun.get_correctness(data_all, cont_diff)
fun_plt.plot_correctness(dat, right_levels, cont_diff, n_trials, 10050, saveplot=False)

