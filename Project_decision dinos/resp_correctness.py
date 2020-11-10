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


# response: -1 is right.
# stimulus direction: negative is right.
response = dat['response']
stim_dir = dat['contrast_left'] - dat['contrast_right']
keys = ['r_cct', 'r_incct', 'l_cct', 'l_incct', 'zero_cct', 'zero_incct', 'all'] 
n = len(keys)

vals = np.empty([n,9]) # len(keys) should be 5.
vals[:] = np.nan
right_levels = dict(zip(keys,vals))
idx = dict(zip(keys, np.empty([n,1])))
n_trials = dict(zip(keys,np.empty([n,1])))

correctness = (np.sign(response)==np.sign(stim_dir))
idx_correct = np.where(correctness==True)[0]
idx_incorrect = np.where(correctness==False)[0]
# unique, counts = np.unique(correctness, return_counts=True) 

idx['r_cct'] = np.where(response==-1)[0]
idx['r_incct'] = np.where(response==-1)[0]
idx['l_cct'] = np.where(response==1)[0]
idx['l_incct'] = np.where(response==1)[0]
idx['zero_cct'] = np.where(response==0)[0]
idx['zero_incct'] = np.where(response==0)[0]
# idx['all'] = np.linspace(0,len(response)-1,len(response))

for i,key in enumerate(keys[0:-1]):
    # print(i, key)
    if i%2==0: # Correct Trials
        # print('correct')
        temp_bool = np.isin(idx[key], idx_correct)
        idx[key] = idx[key][temp_bool]
    elif i%2==1: #Incorrect Trials
        # print('incorrect')
        temp_bool = np.isin(idx[key], idx_incorrect)
        idx[key] = idx[key][temp_bool]
    
    if idx[key][-1]==len(response)-1:
        idx[key] = np.delete(idx[key],-1)
        print('The last index in', key, 'is deleted.')
    n_trials[key] = len(idx[key])


# Compute % rightward for each key (response direction and correct/incorrect)
for key in keys:
    print(key)
    if key=='all':
        right_levels[key] = fun.get_rightward(dat, stim_dir)
        n_trials[key] = len(response)
    else:
        # Compute % rightward for each instance
        i_temp = []
        for i, val in enumerate(np.unique(stim_dir)):
            arr = (idx[key]+1)[stim_dir[idx[key]+1]==val]
            if len(arr) == 0:
                print('arr is empty! check val=',val)
                i_temp.append(i)
            right_levels[key][i] = np.divide(sum(response[arr]<0),len(arr), out=np.zeros(1), where=len(arr)!=0)*100
        right_levels[key][i_temp]=np.nan # replace the empty element with NaN
# return right_levels, 

colors, _, _ = fun.get_colors()
fig = plt.figure(figsize=(8,6))
xdata = np.unique(stim_dir)
plt.plot(xdata, 100-right_levels['all'],'ro-', label='All (%1.0f)'%n_trials['all'], alpha=0.5, linewidth=3)

plt.plot(xdata, 100-right_levels['r_cct'],'D-',  color=colors['darkviolet'], 
         label='r_cct (%1.0f)'%n_trials['r_cct'], linewidth=2)
plt.plot(xdata, 100-right_levels['r_incct'],'^:',  color=colors['violet'], 
         label='r_incct (%1.0f)'%n_trials['r_incct'], linewidth=2)
plt.plot(xdata, 100-right_levels['l_cct'],'x--', color=colors['lime'], 
         label='l_cct (%1.0f)'%n_trials['l_cct'], linewidth=2, alpha=0.5)
plt.plot(xdata, 100-right_levels['l_incct'],'x--', color=colors['deeppink'], 
         label='l_incct (%1.0f)'%n_trials['l_incct'], linewidth=2, alpha=0.5)
plt.plot(xdata, 100-right_levels['zero_cct'],'^:',  color=colors['skyblue'], 
         label='zero_cct (%1.0f)'%n_trials['zero_cct'], linewidth=2)
plt.plot(xdata, 100-right_levels['zero_incct'],'D-',  color=colors['dodgerblue'], 
         label='zero_incct (%1.0f)'%n_trials['zero_incct'], linewidth=2)

plt.xlabel('Contrast difference')
plt.ylabel('1-Leftward (%)')
plt.title('Session: %1.0f, '%n_session + dat['mouse_name'], fontsize=16)
plt.legend(loc='upper left', fontsize=10)
plt.grid()
fig.show()
