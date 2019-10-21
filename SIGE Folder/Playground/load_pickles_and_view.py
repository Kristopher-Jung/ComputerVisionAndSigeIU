#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 18:45:23 2019

@author: david
"""
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
import json
import pickle

# path = "/home/david/ComputerVisionIU2019/Playground/"
# os.chdir(path)


#with open('UHF_TYT_DMR_dtmf1_snr_hi.sigmf-data_bounded_raw.pickle', 'rb') as bounded:
#    bounded_data = pickle.load(bounded)
#with open('UHF_TYT_DMR_dtmf1_snr_hi.sigmf-data_bounded_padded.pickle', 'rb') as padded:
#    padded_data = pickle.load(padded) 


#with open('UHF_lora125_db_snr_hi.sigmf-data_bounded_raw.pickle', 'rb') as bounded:
#    bounded_data = pickle.load(bounded)
#with open('UHF_lora125_db_snr_hi.sigmf-data_bounded_padded.pickle', 'rb') as padded:
#    padded_data = pickle.load(padded) 

with open('UHF_TYT_DMR_dtmf1_snr_hi_Sun_Sep_29_18_58_39_2019_bound_0_raw.pickle', 'rb') as padded:
    loaded = pickle.load(padded)

padded_data = loaded['bounded']
#temp = padded_data[0,0,:,:]  
#print('padded type = ', type(padded_data))    
#plt.imshow(np.log( padded_data[0,0:300,0:700] + 1e-3) , origin='lower', aspect='auto', cmap='magma')

print(np.shape(padded_data))


fig=plt.figure(figsize=(10, 5))
columns = 2
rows = 1

#fig1 = np.log(padded_data[0,0,:,:]+ 0, size=(h,w))
#fig2 = np.log(padded_data[1,0,:,:]+ 0, size=(h,w))

fig1 = np.log(padded_data[0,:,:]+ 0)
#fig2 = np.log(padded_data[1,0,:,:]+ 0)

fig.add_subplot(1, 1, 1)
plt.imshow(fig1)
#fig.add_subplot(2, 1, 2)
#plt.imshow(fig2)
plt.show()



#plt.imshow(np.log(padded_data[0,0,:,:]+ 0) , origin='lower', aspect='auto', cmap='magma') 
#plt.imshow(np.log(padded_data[1,0,:,:]+ 0) , origin='lower', aspect='auto', cmap='magma')
#plt.imshow(np.log(padded_data[2,0,:,:]+ 0) , origin='lower', aspect='auto', cmap='magma') 
#plt.imshow(np.log(padded_data[3,0,:,:]+ 0) , origin='lower', aspect='auto', cmap='magma') 
#plt.imshow(np.log(padded_data[4,0,:,:]+ 0) , origin='lower', aspect='auto', cmap='magma') 
#plt.imshow(np.log( padded_data[0,0:200,0:200]+ 0) , origin='lower', aspect='auto', cmap='magma')  
   