# Import Libraries

import math
import numpy as np 
from numpy.random import choice
from PIL import Image
from scipy.io import wavfile
import PIL

from colormap import rgb2hex, hex2rgb
import re
import os
from abc import ABC


class SGE(ABC):
    
    def __init__(self, path) -> None:
        self.path = path
        self.buffer_symbols = ['a', 'b', 'c', 'd', 'e']
        
    def encode(self):
        
        samplerate, s_arr = wavfile.read(self.path)
        resolution = math.ceil(np.sqrt(len(s_arr)))
        delta_res = resolution ** 2 - len(s_arr)
        
        new_arr = []
        srate_rgb = int(samplerate ** (1/3))
        s_rate_buffer = [[srate_rgb, srate_rgb, srate_rgb] for x in range(delta_res)]
        
        for elem in s_arr:
            gate = choice([False, True])
            
            app = None
            
            salt_positive = ''.join([choice(self.buffer_symbols) for i in range(6 - len(str(elem)))])
            salt_negative = ''.join([choice(self.buffer_symbols) for i in range(6 - len(str(elem)))])
        
            if elem >= 0:
                
                if gate:
                    app = f'#{elem}' + salt_positive
                else:
                    app = f'#{salt_positive}{elem}'
                new_arr.append(app)
                
            else:
                
                if gate:
                    app = f'#f{-elem}' + salt_negative
                else:
                    app = f'#f{salt_negative}{-elem}'
                
                new_arr.append(app)
                
                
        p_arr = np.array([list(hex2rgb(x)) for x in new_arr] + s_rate_buffer)
        p_arr = p_arr.reshape(resolution, resolution, 3)
        p_arr = p_arr.astype(np.uint8)
        
        img = Image.fromarray(p_arr)
        img.save(f'{self.path[:-4]}_encoded.png')
        
        
        

codec = SGE('test.wav')
codec.encode()