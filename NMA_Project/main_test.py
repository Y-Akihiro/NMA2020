#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:23:20 2021

@author: akihiro

main_test.py
"""


# ====================== Test Stuff ======================
# Testing box plot (difficulty & response. This doesn't include
#                   zero difference & no go case.) 
langs = ['hard_l', 'easy_l', 'zero_l', 'all', 'zero_r', 'easy_r', 'hard_r']
#  -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#  -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#  -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# This categorization should be (for the stimulus psychometric curve)
langs = ['hard_l', 'hard_r', 'hard_z', 'all', 'easy_z', 'easy_r', 'easy_l']

#  -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#  -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
#  -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
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
