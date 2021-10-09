# Import Libraries

import math
import numpy as np 
from PIL import Image
from scipy.io import wavfile
import PIL

from colormap import rgb2hex, hex2rgb
import re
import os

def encode(file: str) -> PIL.PngImagePlugin.PngImageFile:
    
    """ Audio track encoding function.
        It takes a .wav file as input and encodes first in HEX and then in RGB.
        The output is an image with audio encoded in it
    """
    
    srate , s_arr = wavfile.read(file)
    resolution = math.ceil(np.sqrt(len(s_arr)))
    delta_res = resolution**2 - len(s_arr)
    
    new_arr = []

    # Symbols to make "salt" in hex-code
    buffer_symbols = ['a', 'b', 'c', 'd', 'e']
    
    # resize samplerate to encode it in last pixel
    srate_rgb = int(srate ** (1/3))
    
    
    # Main encoding loop
    for elem in s_arr:   
        gate = np.random.choice([False, True])
        app = None
        salt_pos = ''.join([np.random.choice(buffer_symbols) for _ in range(6-len(str(elem)))])
        salt_neg = ''.join([np.random.choice(buffer_symbols) for _ in range(6-len(str(elem)))])
        
        if elem >= 0:
            
            if gate:
                app = f'#{elem}' + salt_pos
                new_arr.append(app)
            else:
                app = f'#{salt_pos}{elem}'
                new_arr.append(app)  
        else:
            
            if gate:
            
                app = f'#f{elem*-1}' + salt_neg
                new_arr.append(app)
                
            else:
                app = f'#f{salt_neg}{elem*-1}'
                new_arr.append(app)
            
    p_arr = np.array([list(hex2rgb(x)) for x in new_arr] + [[0,0,0] for x in range(delta_res - 1)] + [[srate_rgb, srate_rgb, srate_rgb]])
    p_arr = p_arr.reshape(resolution, resolution, 3)
    p_arr = p_arr.astype(np.uint8)
    
    # Resize array and make picture from him
    img = Image.fromarray(p_arr)
    img.save(f'{file[:-4]}_encoded.png')
    
def decode(path: str):
    
    """Audio decoding function from image. Uses the inverse algorithm of the encode () function
    """
    
    img = np.array(Image.open(path))
    img = img.reshape(img.shape[0]**2, 3)
    
    f_arr = []
    end_arr = []
    
    for elem in img:
        f_arr.append(rgb2hex(*elem))
        
    for h in f_arr:
        res = None
        if h[1].lower() == 'f':
            res = re.findall('\d+', h)[0]
            res = -int(res)
            end_arr.append(res) 
        else:
            
            res = re.findall('\d+', h)[0]
            end_arr.append(int(res))
            
    end_arr = np.array(end_arr).astype(np.int16)
    
    samplerate = img[-1][-1] ** 3
    samplerate -= samplerate % -100
       
    wavfile.write(f'{path[:-4]}_decoded.wav', samplerate, end_arr)
    
    os.system(f'ffmpeg -i {path[:-4]}_decoded.wav -ar 44100 {path[:-4]}_decoded.mp3')
    os.remove(f'{path[:-4]}_decoded.wav')