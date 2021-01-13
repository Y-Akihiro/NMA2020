# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:08:45 2021

@author: Akihiro

NMA Project
Steinmetz Dataset 

Superstition psychometric curve check

*Run after "main_behavior_analysis.py"

"""

import numpy as np
import matplotlib.pyplot as plt
import functions_get_ as fun

from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


def get_belief(dat):
    '''
    Previous choice & correct/incorrect info.
    1. get response (in original data)
    2. get correct/incorrect info (compare response and contrast difference)
    3. get the indices of trials with previous l/r/z with c/ic
    x. plot psychometric curve
    
    Inputs
    *
    
    Output
    * idx_RL[keys] - indices of right-correct/right-incorrect/etc. (keys)
    * right_levels[keys] - % rightward for each dictionary key
    
    '''
    
    # key for the dictionary with corresponding idx = 0 to 6.
    keys = ['left_c', 'right_c', 'zero_c', 'all', 'zero_ic', 'right_ic', 'left_ic'] 
    n = len(keys)
    vals = np.empty([len(keys),9]) # len(keys) should be 7.
    vals[:] = np.nan
    
    # Construct a dictionary
    right_levels = dict(zip(keys,vals))
    
    response=dat['response'] # all responses (340 for session 11)
    stimulus = dat['contrast_left'] - dat['contrast_right']
        
    cont_diff = stimulus 
    
    # Boolean array (correct or incorrect)
    c = (np.sign(response) == np.sign(stimulus))
    
    # idx_c = np.array([i for i, x in enumerate(c) if x]) # correct trial index
    # idx_ic = np.array([i for i, x in enumerate(c) if not x]) # incorrect trial index
    
    # List of empty integer arrays. Prepare to store lists of indices. (n=7)    
    idx_RL = [[np.empty(0, int)]*1]*n 
    
    # Assign indices of the correct choices for each response
    idx_RL[0] = np.array([i for i, x in enumerate(response>0) if x and c[i]])
    idx_RL[1] = np.array([i for i, x in enumerate(response<0) if x and c[i]])
    idx_RL[2] = np.array([i for i, x in enumerate(response==0) if x and c[i]])
    # For "ALL" trials (340 trials for session 11)
    idx_RL[3] = np.linspace(0,len(response)-1,len(response)).astype(int)
    
    # Assign indices of the incorrect choices for each response
    idx_RL[4] = np.array([i for i, x in enumerate(response==0) if x and not c[i]])
    idx_RL[5] = np.array([i for i, x in enumerate(response<0) if x and not c[i]])
    idx_RL[6] = np.array([i for i, x in enumerate(response>0) if x and not c[i]])
    
    # Fill the %right choice for each of 9 contrast differences
    for j in range(n):
        # Skip this process for 'all' case (index of 3)
        if j != 3:
            # check the contrast differences (unique) and the number of occurences (counts)
            if len(response)-1 in idx_RL[j]:
                idx_RL[j] = idx_RL[j][:-1]
            unique, counts = np.unique(cont_diff[idx_RL[j]+1], return_counts=True)
    
            print('unique cont_diff size:', np.unique(cont_diff[idx_RL[j]+1]).size, keys[j])
            unq_values = np.unique(cont_diff[idx_RL[j]+1]) # unique values for the 'current' trials.
            
            for i, val in enumerate(unq_values): # Assumption: cont_diff[i] has all the 9 contrast differences.
            #     print(i,':', val)
                resp = dat['response'][idx_RL[j]+1][cont_diff[idx_RL[j]+1]==val]
                array_indx = int(4*val + 4) # convert the contrast difference value to the corresponding array index
                right_levels[keys[j]][array_indx] = np.count_nonzero(resp<0) / counts[i]*100 # right choice
    
    right_levels["all"] = fun.get_rightward(dat, cont_diff)
    
    print('all trial data is added.')

    return idx_RL, right_levels, keys

def plt_belief(dat, n_session, cont_diff, rightward, srcdir,
               idx_RL, right_levels, keys, saveplot=False):
    '''
    Input
    * cont_diff
    * rightward
    * right_levels
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
    plt.title('Session: %1.0f, '%n_session + dat['mouse_name']+' (superstition)', 
    		  fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    
    plt.grid(alpha=0.4)
    fig.show()

    if saveplot:
        print('Saving a figure to', srcdir)
        plt.savefig('belief_'+str(n_session)+'.png')
        plt.close(fig)

def plt_belief_mice(dat, name, cont_diff, rightward, srcdir,
               idx_RL, right_levels, keys, saveplot=False):
    '''
    Input
    * cont_diff
    * rightward
    * right_levels
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


if __name__ == "__main__":
    
    idx_RL, right_levels, keys = get_belief(dat)
    plt_belief(dat, n_session, cont_diff, rightward, srcdir,
               idx_RL, right_levels, keys, saveplot=False)
