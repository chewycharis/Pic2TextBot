import cv2
import numpy as np 
import pytesseract as ts

## should work for regular text and fb messages ## 

def load_image(img_path):
    im_cv=cv2.imread(img_path)
    return cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)

def show_image(img):
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)     
    imS = cv2.resize(img, (540,960))               
    cv2.imshow("output", imS)                      
    cv2.waitKey(0)   

    
def crop(img):
    y_max=np.shape(img)[0]
    crop_y_min=int(0.09*y_max)
    crop_y_max=int(0.94*y_max)
    crop_img = img[crop_y_min:crop_y_max,:]
    return crop_img

def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def light_mode_filter(img):
    t=np.copy(img)
    t[t>250]=0
    t[t>90]=255
    return t

def dark_mode_filter(img):
    t=np.copy(img)
    t[t<250]=0
    return t

def detect_mode(img):
    m=np.mean(img[:,0])
    if m <127.5:
        mode="dark"
    else:
        mode="light"
    return mode

def filter_by_mode(img):
    mode=detect_mode(img)
    if mode=="dark":
        return dark_mode_filter(img)
    else:
        return light_mode_filter(img)

def translate_image(img):
    return ts.image_to_string(img)