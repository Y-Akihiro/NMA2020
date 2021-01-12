# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 09:07:18 2020

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
# from matplotlib import pyplot as plt


def main():
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Plot psychometric curves for all sessions:    
    for n_session in range(len(alldat)):
        dat, barea, NN, regions, brain_groups, nareas = fun.load_data(n_session, alldat)    
        _, _, cont_diff, _, _, _ = fun.get_task_difference(n_session, dat)
        rightward = fun.get_rightward(dat, cont_diff)
        idx_RL, right_levels = fun.get_right_history(dat, cont_diff)
        response = dat['response']
        
        # fun_plt.plot_psychometric(cont_diff, rightward, response, right_levels,
        #                           idx_RL, n_session, dat, srcdir, savefig=True)
        # langs, diff_mean, diff_std = fun.get_bars_data(right_levels)
        # fun_plt.plot_bars(langs, diff_mean, diff_std, srcdir, n_session, saveplot=True)
        
        # right_levels, keys, n_trials = fun.get_right_hist_1(dat, cont_diff)
        # fun_plt.plot_stim_dir(n_session, dat, cont_diff, right_levels, keys, n_trials, saveplot=True)

        print(n_session)


if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath(__file__)))
    # print(os.getcwd())
    
    main()
