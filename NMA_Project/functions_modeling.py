#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 09:55:46 2021

@author: akihiro

List of functions for behavior modeling

"""

import os, requests
import numpy as np

from IPython.display import HTML
import random


def logistic_function(x,x0, y0, a,b):
    '''
    Four-parameter logistic function for model fitting
    '''
    return y0 + a/(1+np.exp(-(x-x0)/b))



