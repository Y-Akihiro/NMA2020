# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:51:09 2020

@author: Akihiro Yamaguchi

Script for Steinmetz behavior data analysis.
"""

import numpy as np
# import pandas as pd
import os
# import requests
import matplotlib.cm as cm
colormap = cm.viridis

import functions as fun # functions for analysis, loading data, etc.
import Steinmetz_functions as fun_plt # Functions for plotting

# import matplotlib and set defaults
from matplotlib import pyplot as plt

# ===================== for plotting =====================
# Sort colors by hue, saturation, value and name.
from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
sorted_names = [name for hsv, name in by_hsv]
# ==============================================================

# from matplotlib import rcParams 
# rcParams['figure.figsize'] = [20, 4]
# rcParams['font.size'] =15
# rcParams['axes.spines.top'] = False
# rcParams['axes.spines.right'] = False
# rcParams['figure.autolayout'] = True


def main():
    
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
    # % rightward at each contrast difference
    rightward = fun.get_rightward(dat, cont_diff) 
    
    # check the contrast differences and the number of occurences
    unique, counts = np.unique(cont_diff, return_counts=True) 
    print('Contrast difference and no. of trials:')
    for i,val in enumerate(unique): print(val, ':', counts[i])
    # print(dict(zip(unique, counts)))
    
    # Get data to make a psychometric curve for response+difficulty
    idx_RL, right_levels = fun.get_right_history(dat, cont_diff)
    response = dat['response']
    
    # Prepare for a bar plot 
    langs, diff_mean, diff_std = fun.get_bars_data(right_levels)
    right_levels2, keys, n_trials = fun.get_right_hist_1(dat, cont_diff)
    
    # ====================== Plot Stuff Begins ======================
    # ===============================================================
    # Plot response and contrast difference for one session
    fun_plt.plot_resp_contDiff(dat, cont_diff, n_session)

    # Plot one psychometric curve for 'all' data 
    fun_plt.plot_1psychometric(cont_diff, rightward, n_session, dat)

    # Plot psychometric curve for all responses + difficulties 
    fun_plt.plot_psychometric(cont_diff, rightward, response, right_levels, 
                              idx_RL, n_session, dat, srcdir)
    
    # Make a bar plot that corresponds to the following psychometric curve
    fig0, ax0 = plt.subplots(1,1)
    fun_plt.plot_bars(langs, diff_mean, diff_std, srcdir, n_session)

    # Plot psychometric curve with stimulus direction history.
    fun_plt.plot_stim_dir(n_session, dat, cont_diff, right_levels2, keys, n_trials, saveplot=False)

    # =============================================================
    # ====================== Plot Stuff Ends ======================

    
    # ====================== Test Stuff ======================
    # Testing box plot
    langs = ['hard_l', 'easy_l', 'zero_l', 'all', 'zero_r', 'easy_r', 'hard_r']  
    vals = np.empty([7,9])
    vals[:]=np.nan
    
    test_data = dict(zip(langs, vals))
    for i, key in enumerate(langs):
        print(key)
        test_data[key] = rightward[~np.isnan(right_levels[key])] - right_levels[key][~np.isnan(right_levels[key])]
        # diff_mean[i] = np.mean(rightward[~np.isnan(right_levels[key])] 
        #                 - right_levels[key][~np.isnan(right_levels[key])])
        # diff_std[i] = np.std(rightward[~np.isnan(right_levels[key])] 
        #                 - right_levels[key][~np.isnan(right_levels[key])])
        langs[i] = key+'(%1.0f)'%len(right_levels[key][~np.isnan(right_levels[key])])

    fig1, ax1 = plt.subplots(1,1)
    ax1.boxplot(test_data['hard_r']) # Both plt.boxplot() or plt.bar() might work.
    # for tick, label in 
    # ax1.text
    
    # Get the average over all sessions
    test = np.zeros([7,len(alldat),2])
    
    for n_session in range(len(alldat)):
        print('session ', str(n_session))
        dat, barea, NN, regions, brain_groups, nareas = fun.load_data(n_session, alldat)    
        _, _, cont_diff, _, _, _ = fun.get_task_difference(n_session, dat)
        rightward = fun.get_rightward(dat, cont_diff)
        idx_RL, right_levels = fun.get_right_history(dat, cont_diff)
        
        langs, diff_mean, diff_std = fun.get_bars_data(right_levels)
        
        test[:,n_session,0] = diff_mean
        test[:,n_session,1] = diff_std
    
    val_mean = np.mean(test[:,:,0], axis=1)
    plt.bar(langs, val_mean)
    
    
if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath(__file__)))
    # print(os.getcwd())
    
    main()
