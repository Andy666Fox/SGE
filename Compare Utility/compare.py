"""Script for comparing the original and decoded file. Provides a summary of the standard deviation, mean values, and a small visualization.
"""

import math
import numpy as np 
from scipy.io import wavfile
import  matplotlib.pyplot as plt
from abc import  ABC
from prettytable import PrettyTable


class Compare(ABC):
    
    def __init__(self, wav1: str, wav2: str) -> None:
        self.n1, self.n2 = wav1, wav2
        self.srate1, self.wav1 = wavfile.read(wav1)
        self.srate2, self.wav2 = wavfile.read(wav2)
        
    
    def table(self):
        std1 = np.std(self.wav1)
        std2 = np.std(self.wav2)
        l1 = f'{str(len(self.wav1))} samples'
        l2 = f'{str(len(self.wav2))} samples'
        m1 = np.mean(self.wav1)
        m2 = np.mean(self.wav2)
    
        tb = PrettyTable()
        tb.field_names = ['Criterion', self.n1, self.n2]
        tb.add_row(['STD', std1, std2])
        tb.add_row(['LENGHT', l1, l2])
        tb.add_row(['MEAN', m1, m2])
        
        print(tb)
        
    def compare(self, log=False):

        res = (np.sum(self.wav1) / np.sum(self.wav2)) * 100
        convergence = res if res > 0 else 0
        
        pl1 = np.log(self.wav1) if log else self.wav1
        pl2 = np.log(self.wav2) if log else self.wav2
        
        fig, axs =   plt.subplots(2)
        fig.suptitle(f'Files convergence: {str(convergence)[:5]} % \n Percentage of losses: {str(100 - convergence)[:5]} %')
        axs[0].plot(pl1, label=f'WAV1 srate: {self.srate1}', color='red')
        axs[1].plot(pl2, label=f'WAV2 srate:{self.srate2}', color='orange')   
        fig.legend() 
        plt.show()
        
    def all_compare(self):
        self.table()
        self.compare()
        
        
wav1 = input('Enter first filepath: ')
wav2 = input('Enter second filepath:')
conv = Compare(wav1, wav2)
conv.all_compare()