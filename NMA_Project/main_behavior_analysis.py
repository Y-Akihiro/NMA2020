# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:51:09 2020

@author: Akihiro Yamaguchi

Script for Steinmetz behavior data analysis.
"""

# ===================== libraries & functions =====================
import numpy as np
import os
# import requests
# import pandas as pd
import functions_get_ as fun        # functions to load data, analyze, etc.

# ===================== for plotting =====================
from matplotlib import pyplot as plt
import matplotlib.cm as cm
colormap = cm.viridis
import functions_plot_ as fun_plt   # Functions for plotting

colors, _, _ = fun.get_colors()
# =========================================================

def main():
    
    fname = []                  # initialize the list
    fname = fun.load_names()
    print(fname)

    srcdir = os.getcwd()        # get and print the current directory
    print('Current directory is...', srcdir)

    # ====================== Lost Stuff ======================
    alldat = np.array([])
    for j in range(len(fname)):
        alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))
    
    # =========== Load data for a selected session ===========
    n_session = 11
    dat, barea, NN, regions, brain_groups, nareas = fun.load_data(n_session, alldat)    
    cont_diff = dat['contrast_left'] - dat['contrast_right']

    # ====================== Compute Stuff ======================
    # % rightward for each contrast difference
    rightward, unique, counts = fun.get_rightward(dat, cont_diff) 
    
    # Print the contrast differences and the number of occurences
    print('Contrast difference and no. of trials:')
    for i,val in enumerate(unique): print(val, ':', counts[i])
    # print(dict(zip(unique, counts)))
    
    # Get data to make a psychometric curve for response+difficulty
    idx_RL, right_levels = fun.get_choice_dep_rightward(dat, cont_diff)
    
    # Prepare for a bar plot 
    # langs, diff_mean, diff_std = fun.get_bars_data(right_levels) # There's some errors
    right_levels2, keys, n_trials = fun.get_stim_dep_rightward(dat, cont_diff)

    
    # ====================== Plot Stuff Begins ======================
    # ===============================================================
    response = dat['response']

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
    fun_plt.plot_stim_dir(n_session, dat, cont_diff, right_levels2, 
                          keys, n_trials, saveplot=False)

    # =============================================================
    # ====================== Plot Stuff Ends ======================

    
    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath(__file__)))
    # print(os.getcwd())
    
    main()
