# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:51:09 2020

@author: Akihiro
"""

import numpy as np
# import pandas as pd
# import os, requests
import matplotlib.cm as cm
colormap = cm.viridis

import functions as fun # functions for analysis, loading data, etc.
import Steinmetz_functions as fun_plt # Functions for plotting

# import matplotlib and set defaults
from matplotlib import rcParams 
# from matplotlib import pyplot as plt

rcParams['figure.figsize'] = [20, 4]
rcParams['font.size'] =15
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
rcParams['figure.autolayout'] = True

fname = [] # initialize the list
fname = fun.load_names()
print(fname)

def main():
    # Load Data:
    alldat = np.array([])
    for j in range(len(fname)):
        alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))
    
    # ==========================================
    n_session = 11
    dat, barea, NN, regions, brain_groups, nareas = fun.load_data(n_session, alldat)    
    _, _, cont_diff, _, _, _ = fun.get_task_difference(n_session, dat)

    fun_plt.plot_resp_contDiff(dat, cont_diff)

    rightward = fun.get_rightward(dat, cont_diff)
    # ==========================================
    
    # Plot one psychometric function
    fun_plt.plot_1psychometric(cont_diff, rightward, n_session, dat)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    unique, counts = np.unique(cont_diff, return_counts=True) # check the contrast differences and the number of occurences
    
    print('Contrast difference and no. of trials:')
    for i,val in enumerate(unique): print(val, ':', counts[i])
    # print(dict(zip(unique, counts)))
    
    # Plot a psychometric curve:
    idx_RL, right_levels = fun.get_right_history(dat, cont_diff)
    fun_plt.plot_psychometric(cont_diff, rightward, response, right_levels, idx_RL, n_session, dat)

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    
    
# ===================== for plotting stuff =====================
# Sort colors by hue, saturation, value and name.
from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                for name, color in colors.items())
sorted_names = [name for hsv, name in by_hsv]
# ==============================================================

    
if __name__ == "__main__":
    
    main()