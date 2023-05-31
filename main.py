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
    
def read_image(image_path):
    '''
    Read image from path
    
    Parameters
    ----------
    image_path : str
        Path of the image to be read
        
    Returns
    -------
    np.ndarray: Image array
    '''
    return cv2.imread(image_path)


def steganography_image(image,data,shift):
    '''
    Embeds data into image
    
    Parameters
    ----------
    image : np.ndarray
        Image to be embedded with data
    data : str
        Data to be embedded
    shift : int
        Shift value to be used for embedding
        
    Returns
    -------
    np.ndarray: Image array with embedded data
    '''
    # Calculate maximum bytes to be embedded
    max_bytes = image.shape[0] * image.shape[1] * 3 // 8
    # Check if the number of bytes to be embedded is less than the maximum bytes
    if len(data) > max_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
    # Embed data into image
    data_index = 0
    binary_data = msg_to_bin(data)
    data_len = len(binary_data)
    for values in image:
        for pixel in values:
            r, g, b = msg_to_bin(pixel)
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image

def decode_binary_string(s):
    decode_text =  ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
    return decode_text[:-5]

def steganography_endoce_image(image,data,choose_rgb,shift=3):
    '''
    Embeds data into image
    
    Parameters
    ----------
    image : np.ndarray
        Image to be embedded with data
    data : str
        Data to be embedded
    choose_rgb : int
        Choose which rgb to be embedded(0:R,1:G,2:B)
    shift : int
        Shift value to be used for embedding
        
    Returns
    -------
    np.ndarray: Image array with embedded data
    '''

    copy_image = image.copy()
    # Calculate maximum bytes to be embedded
    max_bytes = ((copy_image.shape[0] * copy_image.shape[1] // 8) / shift) - 5
    # Check if the number of bytes to be embedded is less than the maximum bytes
    if len(data) > max_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
    # Embed data into image
    data_index = 0
    data += "#####"
    binary_data = msg_to_bin(data)
    data_len = len(binary_data)
    for i in range(copy_image.shape[0]):
        for j in range(0,copy_image.shape[1],shift):

            rgb = msg_to_bin(copy_image[i][j][choose_rgb])
            if data_index < data_len:
                if rgb[-1] != binary_data[data_index]:
                    if rgb[-1] == '1':
                        copy_image[i][j][choose_rgb] -= 1
                    else:
                        copy_image[i][j][choose_rgb] += 1
                    data_index += 1
                else:
                    data_index += 1
            if data_index >= data_len:
                break

    return copy_image

def steganography_decode_image(image,choose_rgb,shift):
    '''
    Extracts data from image
    
    Parameters
    ----------
    image : np.ndarray
        Image to be embedded with data
    choose_rgb : int
        Choose which rgb to be embedded(0:R,1:G,2:B)
    shift : int
        Shift value to be used for embedding
        
    Returns
    -------
    str: Extracted data
    '''
    copy_image = image.copy()
    binary_data = ""
    for i in range(copy_image.shape[0]):
        for j in range(0,copy_image.shape[1],shift):
            rgb = msg_to_bin(copy_image[i][j][choose_rgb])
            binary_data += rgb[-1]
            # print(binary_data)
            if binary_data[-40:] == '0010001100100011001000110010001100100011':
                decode_text_data = decode_binary_string(binary_data)
                return  decode_text_data

def main():
    original_image = cv2.imread('photo/windows.jpg')
    stegano_image = steganography_endoce_image(image=original_image,data="Hello World Enes Geliyor",choose_rgb=1,shift=5)
    # cv2.imshow("Original image",original_image)
    # cv2.imshow("Steganography image",stegano_image)
    print((original_image==stegano_image).all())
    decode_data = steganography_decode_image(image=stegano_image,choose_rgb=1,shift=5)
    print(decode_data)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()