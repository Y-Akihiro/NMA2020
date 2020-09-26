# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 11:11:19 2020

@author: Akihiro

List of functions 
"""
import os, requests
import numpy as np

from IPython.display import HTML
import random

def hide_toggle(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'Toggle show/hide'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current, 
        toggle_text=toggle_text
    )

    return HTML(html)

def load_names(fname=[]):
    del fname
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
    return fname

def load_data(n_session, alldat):
    '''
    
    '''
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
        * response of -1 corresponds to 'right' and 1 to 'left' choices
    """
    rightward = np.zeros(len(np.unique(cont_diff)))
    unique, counts = np.unique(cont_diff, return_counts=True) # check the contrast differences and the number of occurences

    for i, val in enumerate(np.unique(cont_diff)):
        resp = dat['response'][cont_diff==val]
        rightward[i] = np.count_nonzero(resp<0) / counts[i]*100
        
    return rightward

def func(x,x0, y0, a,b):
    '''
    Four-parameter logistic function for model fitting
    '''
    return y0 + a/(1+np.exp(-(x-x0)/b))

def get_right_hist_1(dat, cont_diff):
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


def get_right_hist_2(dat, cont_diff):
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
    easy_l = (cont_diff==-1) + (cont_diff==-0.75)
    diff_l = (cont_diff==-0.25) + (cont_diff==-0.5)
    diff_r = (cont_diff==0.25) + (cont_diff==0.5)
    easy_r = (cont_diff==1) + (cont_diff==0.75)

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

        if hist in unique[0:2]: # easy left
            reasy_l[n_el, idx_cont,0] = dat['response'][i+1]
            reasy_l[0,idx_cont,1] +=1
            n_el += 1
        elif hist in unique[2:4]: # difficult left
            rdiff_l[n_dl, idx_cont,0] = dat['response'][i+1]
            rdiff_l[0, idx_cont,1] += 1
            n_dl += 1
        elif hist in unique[5:7]: # difficult right
            rdiff_r[n_dr, idx_cont,0] = dat['response'][i+1]
            rdiff_r[0, idx_cont,1] += 1
            n_dr += 1
        elif hist in unique[7:9]: # easy right
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
