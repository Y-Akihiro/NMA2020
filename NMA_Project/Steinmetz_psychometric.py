# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:26:26 2020

@author: Akihiro
"""

import numpy as np
import pandas as pd
import os, requests
import matplotlib.cm as cm
colormap = cm.viridis

# import matplotlib and set defaults
from matplotlib import rcParams 
from matplotlib import pyplot as plt
rcParams['figure.figsize'] = [20, 4]
rcParams['font.size'] =15
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
rcParams['figure.autolayout'] = True

import Steinmetz_functions as fun



