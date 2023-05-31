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

def decode_binary_string(s):
    decode_text =  ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
    return decode_text[:-5]

def steganography_endoce_image(image,data,choose_rgb,row_shift=3,column_shift=3):
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
    row_shift : int
        Row shift value to be used for embedding
    column_shift : int
        Column shift value to be used for embedding
        
    Returns
    -------
    np.ndarray: Image array with embedded data
    '''

    copy_image = image.copy()
    data += "#####"
    # Calculate maximum bytes to be embedded
    max_bytes = ((copy_image.shape[0]/row_shift) * (copy_image.shape[1]/column_shift) // 8)
    # Check if the number of bytes to be embedded is less than the maximum bytes
    if len(data) > max_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
    # Embed data into image
    data_index = 0
    binary_data = msg_to_bin(data)
    data_len = len(binary_data)
    for i in range(0,copy_image.shape[0],row_shift):
        for j in range(0,copy_image.shape[1],column_shift):

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

    cv2.imwrite("photo/encryption_image.jpg", copy_image)

    return copy_image

def steganography_decode_image(image,choose_rgb,row_shift,column_shift):
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
    for i in range(0,copy_image.shape[0],row_shift):
        for j in range(0,copy_image.shape[1],column_shift):
            rgb = msg_to_bin(copy_image[i][j][choose_rgb])
            binary_data += rgb[-1]
            # print(binary_data)
            if binary_data[-40:] == '0010001100100011001000110010001100100011':
                decode_text_data = decode_binary_string(binary_data)
                return  decode_text_data

def main():
    original_image = cv2.imread('photo/windows.jpg')
    stegano_image = steganography_endoce_image(image=original_image,data="Hello World",choose_rgb=1,row_shift=216,column_shift=21)
    # cv2.imshow("Original image",original_image)
    # cv2.imshow("Steganography image",stegano_image)
    print((original_image==stegano_image).all())
    decode_data = steganography_decode_image(image=stegano_image,choose_rgb=1,row_shift=216,column_shift=21)
    print(decode_data)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()