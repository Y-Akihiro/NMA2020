# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:28:12 2020

@author: Akihiro
"""
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)


def download_data():
    # Downlaod Data
    fname = []
    for j in range(3):
        fname.append('steinmetz_part%d.npz'%j)
    url = ["https://osf.io/agvxh/download"]
    url.append("https://osf.io/uv3mw/download")
    url.append("https://osf.io/ehmw2/download")
    
    for j in range(len(url)):
        if not os.path.isfile(fname[j]):
            try:
                r = requests.get(url[j])
            except requests.ConnectionError:
                print("!!! Failed to download data !!!")
            else:        
                if r.status_code != requests.codes.ok:
                    print("!!! Failed to download data !!!")
                else:
                    with open(fname[j], "wb") as fid:
                        fid.write(r.content)
    # Data loading
    alldat = np.array([])
    for j in range(len(fname)):
        alldat = np.hstack((alldat, np.load('steinmetz_part%d.npz'%j, allow_pickle=True)['dat']))


    return 

def load_data(n_session):
    dat = alldat[n_session]

    # groupings of brain regions
    regions = ["vis ctx", "thal", "hipp", "other ctx", "midbrain", "basal ganglia", "cortical subplate", "other"]
    brain_groups = [["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"], # visual cortex
                    ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"], # thalamus
                    ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"], # hippocampal
                    ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"], # non-visual cortex
                    ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"], # midbrain
                    ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"], # basal ganglia 
                    ["BLA", "BMA", "EP", "EPd", "MEA"] # cortical subplate
                    ]

    nareas = 4 # only the top 4 regions are in this particular mouse
    NN = len(dat['brain_area']) # number of neurons
    barea = nareas * np.ones(NN, ) # last one is "other"
    for j in range(nareas):
        barea[np.isin(dat['brain_area'], brain_groups[j])] = j # assign a number to each region
        
    return dat, barea, NN, regions, brain_groups, nareas

def get_rightward(dat, cont_diff):
    """
    Inputs: 
        * dat - data 
        * cont_diff - contrast difference between left and right
    Return:
        * rightward - % of mice respond right for each contrast difference
    """
    rightward = np.zeros(len(np.unique(cont_diff)))
    unique, counts = np.unique(cont_diff, return_counts=True) # check the contrast differences and the number of occurences

    for i, val in enumerate(np.unique(cont_diff)):
        resp = dat['response'][cont_diff==val]
        rightward[i] = np.count_nonzero(resp==1) / counts[i]*100
        
    return rightward

def get_right_hist(dat, cont_diff):
    """
    Inputs: 
        * dat - trial data 
        * cont_diff - contrast difference between left and right
    Return:
        * reasy_l - % of mice respond right for each contrast difference, previous trial is easy left
        * rdiff_l - % of mice respond right for each contrast difference, previous trial is difficult left
        * reasy_r - % of mice respond right for each contrast difference, previous trial is easy right
        * rdiff_r - % of mice respond right for each contrast difference, previous trial is difficult right
    """
    unique, counts = np.unique(cont_diff, return_counts=True) # check the contrast differences and the number of occurences

    n_el = n_dl = n_er = n_dr = n_zero = 0
    
    # Define easy/difficult left/right (boolean array)
    easy_l = (cont_diff==-1)    #+ (cont_diff==-0.75)
    diff_l = (cont_diff==-0.25) #+ (cont_diff==-0.5)
    diff_r = (cont_diff==0.25)  #+ (cont_diff==0.5)
    easy_r = (cont_diff==1)     #+ (cont_diff==0.75)

    reasy_l = np.zeros((easy_l.sum(),9,2)) # 59 x 9
    rdiff_l = np.zeros((diff_l.sum(),9,2)) # 52 x 9
    reasy_r = np.zeros((easy_r.sum(),9,2)) # 41 x 9
    rdiff_r = np.zeros((diff_r.sum(),9,2)) # 62 x 9
    rzero = np.zeros(((cont_diff==0).sum(),9,2)) # 126 x 9

    # Check the number of trials for each difficulties 
    n_trials = np.zeros(6)
    n_trials[0] = rzero.shape[0] 
    n_trials[1] = reasy_l.shape[0]
    n_trials[2] = rdiff_l.shape[0]
    n_trials[3] = rdiff_r.shape[0]
    n_trials[4] = reasy_r.shape[0]
    n_trials[5] = dat['spks'].shape[1]
    
    for i in range(len(dat['response'])-1):
        hist = cont_diff[i]                                  # previous trial difficulty (size) & direction (sign)
        idx_cont = np.where(unique==cont_diff[i+1])[0][0]   # current trial difficulty and direction label (9 unique labels)

        if hist == -1: #in unique[0:2]: # easy left
            reasy_l[n_el, idx_cont,0] = dat['response'][i+1]
            reasy_l[0,idx_cont,1] +=1
            n_el += 1
        elif hist == -0.25: #in unique[2:4]: # difficult left
            rdiff_l[n_dl, idx_cont,0] = dat['response'][i+1]
            rdiff_l[0, idx_cont,1] += 1
            n_dl += 1
        elif hist == 0.25: #in unique[5:7]: # difficult right
            rdiff_r[n_dr, idx_cont,0] = dat['response'][i+1]
            rdiff_r[0, idx_cont,1] += 1
            n_dr += 1
        elif hist == 1.0: #in unique[7:9]: # easy right
            reasy_r[n_er, idx_cont,0] = dat['response'][i+1]
            reasy_r[0, idx_cont,1] += 1
            n_er += 1
        elif hist == 0:
            rzero[n_zero, idx_cont,0] = dat['response'][i+1]
            rzero[0, idx_cont,1] += 1
            n_zero += 1
        else:
            hist += 1 # some action. (whatever is fine to pass)
    #         print('Check: something is wrong')

    # Use np.divide(a, b, out=np.zeros(a.shape), where=b!=0) to avoid 0 division error
    r_easyr = np.divide(np.count_nonzero(reasy_r[:,:,0]==1,axis=0),
                        reasy_r[0,:,1], 
                        out=np.zeros(np.count_nonzero(reasy_r[:,:,0]==1,axis=0).shape), 
                        where=(reasy_r[0,:,1]!=0)) * 100
    r_easyl = np.divide(np.count_nonzero(reasy_l[:,:,0]==1,axis=0),
                        reasy_l[0,:,1], 
                        out=np.zeros(np.count_nonzero(reasy_l[:,:,0]==1,axis=0).shape), 
                        where=(reasy_l[0,:,1]!=0)) * 100
    r_diffr = np.divide(np.count_nonzero(rdiff_r[:,:,0]==1,axis=0),
                        rdiff_r[0,:,1], 
                        out=np.zeros(np.count_nonzero(rdiff_r[:,:,0]==1,axis=0).shape), 
                        where=(rdiff_r[0,:,1]!=0)) * 100
    r_diffl = np.divide(np.count_nonzero(rdiff_l[:,:,0]==1,axis=0),
                        rdiff_l[0,:,1], 
                        out=np.zeros(np.count_nonzero(rdiff_l[:,:,0]==1,axis=0).shape), 
                        where=(rdiff_l[0,:,1]!=0)) * 100
    r_zero = np.divide(np.count_nonzero(rzero[:,:,0]==1,axis=0),
                       rzero[0,:,1], 
                       out=np.zeros(np.count_nonzero(rzero[:,:,0]==1,axis=0).shape), 
                       where=(rzero[0,:,1]!=0)) * 100
        
    return r_easyr, r_easyl, r_diffr, r_diffl, r_zero, n_trials

def get_task_difference(n_session):
    dat, barea, NN, regions, brain_groups, nareas = load_data(n_session, alldat)

    dt = dat['bin_size']                  # binning at 10 ms
    NT = dat['spks'].shape[-1]

    l_cont = dat['contrast_left']         # contrast left
    r_cont = dat['contrast_right']        # contrast right
    
    cont_diff = r_cont - l_cont              # contrast difference: right if positive, left if negative
    abs_task_diff = np.abs(r_cont - l_cont)  # absolute contrast difference
    dtask_diff = np.diff(abs_task_diff)      # change in contrast difference (current - previous)
    dtdiff = np.insert(dtask_diff, 0, 0)     # adjust the array size

    return dt, NT, cont_diff, abs_task_diff, dtask_diff, dtdiff

def plot_psychometric(cont_diff, rightward, response, right_levels, idx_RL, n_session, dat):
	'''
	Make a psychometric function.
		
	'''
	xdata = np.unique(cont_diff)
	ydata = rightward

	fig = plt.figure(figsize=(8,6))

	plt.plot(xdata, ydata,'ro-', label='All (%1.0f)'%len(response), alpha=0.5, linewidth=3)

	plt.plot(xdata, right_levels['hard_r'],'D-',  color=colors['darkviolet'], 
	         label='hard_r (%1.0f)'%(idx_RL[1].size), linewidth=2)
	plt.plot(xdata, right_levels['easy_r'],'^:',  color=colors['violet'], 
	         label='easy_r (%1.0f)'%(idx_RL[0].size), linewidth=2)
	plt.plot(xdata, right_levels['zero_r'],'x--', color=colors['lime'], 
	         label='zero_r (%1.0f)'%(idx_RL[2].size), linewidth=2, alpha=0.5)
	plt.plot(xdata, right_levels['zero_l'],'x--', color=colors['deeppink'], 
	         label='zero_l (%1.0f)'%(idx_RL[5].size), linewidth=2, alpha=0.5)
	plt.plot(xdata, right_levels['easy_l'],'^:',  color=colors['skyblue'], 
	         label='easy_l (%1.0f)'%(idx_RL[3].size), linewidth=2)
	plt.plot(xdata, right_levels['hard_l'],'D-',  color=colors['dodgerblue'], 
	         label='hard_l (%1.0f)'%(idx_RL[4].size), linewidth=2)

	plt.xlabel('Contrast difference')
	plt.ylabel('Rightward (%)')
	plt.title('Session: %1.0f, '%n_session + dat['mouse_name'], fontsize=16)
	plt.legend(loc='upper left', fontsize=10)
	plt.show()

def plot_1psychometric(cont_diff, rightward, n_session, dat):
	'''

	'''
	xdata = np.unique(cont_diff)
	ydata = rightward

	fig = plt.figure(figsize=(6,4))

	plt.plot(xdata, ydata,'o-', label=n_session)
	plt.xlabel('Contrast difference')
	plt.ylabel('Rightward (%)')
	plt.title('Session: %1.0f, '%n_session + dat['mouse_name'], fontsize=16)
	plt.legend(loc='upper left', fontsize=10)
	plt.grid()
	plt.show()

def plot_resp_contDiff(dat, cont_diff):
	'''

	'''
	plt.plot(cont_diff,'ro-', label='contrast difference')
	plt.plot(dat['response'],'bo', label='responses: right(+1) and left(-1)')
	plt.legend()
	plt.show()

