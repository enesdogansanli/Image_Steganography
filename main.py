import cv2
import numpy as np
import pandas as pd


def msg_to_bin(msg):  
    '''
    Convert string message to binary
    
    Parameters
    ----------
    msg : str
        Message to be converted to binary
        
    Returns
    -------
    str: Binary representation of the message
    '''
    if type(msg) == str:  
        return ''.join([format(ord(i), "08b") for i in msg])  
    elif type(msg) == bytes or type(msg) == np.ndarray:  
        return [format(i, "08b") for i in msg]  
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:  
        raise TypeError("Input type not supported")  
