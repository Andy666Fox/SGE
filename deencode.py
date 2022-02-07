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


# Sound-Graphic Encoding class
class SGE(ABC):
    
    def __init__(self) -> None:
        self.buffer_symbols: list[str] = ['a', 'b', 'c', 'd', 'e']
        
        
    def encode(self, path_to_file) -> None:
        
        samplerate, s_arr = wavfile.read(path_to_file)
        resolution: int = math.ceil(np.sqrt(len(s_arr)))
        delta_res: int = resolution ** 2 - len(s_arr)
        
        new_arr: list[str] = []
        srate_rgb = int(samplerate ** (1/3))
        s_rate_buffer = [[srate_rgb, srate_rgb, srate_rgb] for x in range(delta_res)]
        
        
        for elem in s_arr:
            gate: bool = choice([False, True])
            
            app = None
            
            salt_positive: str = ''.join([choice(self.buffer_symbols) for i in range(6 - len(str(elem)))])
            salt_negative: str = ''.join([choice(self.buffer_symbols) for i in range(6 - len(str(elem)))])
        
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
        img.save(f'{path_to_file[:-4]}_encoded.png')
        

    def decode(self, path_to_img: str):
        
        im_arr = np.array(Image.open(path_to_img))
        im_arr = im_arr.reshape(im_arr.shape[0]**2, 3)
        
        im_buff = im_arr[:]
        
        im_arr = np.array([rgb2hex(*x) for x in im_arr])
        
        end_arr = []
        
        for h in im_arr:
            
            res = None
            
            res = re.findall('\d+', h)[0]
            end_arr.append(-int(res) if h[1].lower() == 'f' else int(res))

        end_arr = np.array(end_arr).astype(np.int16)
        
        samplerate = im_buff[-1][-1] ** 3
        samplerate -= samplerate % -100
        border = path_to_img.index('_')
        
        wavfile.write(f'{path_to_img[:border]}_decoded.wav', samplerate, end_arr)
        
        try:
            os.system(f'ffmpeg -i {path_to_img[:border]}_decoded.wav -ar 44100 {path_to_img[:border]}_decoded.mp3')
        except Exception as e:
            print(e)
            