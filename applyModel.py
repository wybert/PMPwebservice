# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 11:26:37 2014

@author: zqh
"""


import numpy as np
import cPickle
trained_machine=cPickle.load(file('machine.pkl','rb'))

SH_DataSet=np.load('SH_DataSet.npy')

preDataSet = SH_DataSet

Data,Target=preDataSet[:,1:-1],preDataSet[:,-1] 
date = preDataSet[:,0]

test=trained_machine.predict(Data)



