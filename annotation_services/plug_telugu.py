# ----------------------------------------------------------------------
# This script invokes Tesseract OCR API for telugu language.
# It takes image path as an input an returns annotations
# made by tesseract in the form of a json file.
#
# @author: Vijay Chilaka <cs17b008@iittp.ac.in>
# @date: 15/05/2021
#
#-----------------------------------------------------------------------
import pytesseract
from pytesseract import Output
import numpy as np
from matplotlib import image
import os
import json

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
tessdata_dir_config = r'--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'


def get_annotations_data_telugu(im_path):
    """Obtaining annotations using Tesseract OCR(telugu language).
    This function takes image path as input and invokes Tesseract OCR.
    And then returns the annotations as output in the form of a json string.
    Args:
        im_path: Way to the file where image is available.
    Returns:
        A json string that contains labels and the coordinates of the annotations.
        For example,
            {
                label1 : [x1, y1, x2, y2],
                label2 : [a1, b1, a2, b2]
            }
    """  
    print(im_path)

    img_path = im_path
    json_str = ''
    if(os.path.isfile(img_path)==False):
        print("not a valid image path")
    else: 
        img = image.imread(img_path)
    
    d = pytesseract.image_to_data(img, output_type=Output.DICT, config=tessdata_dir_config,lang="tel")
            
    label_dict = {}
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if(d['text'][i]!=""):
            name=str(d['text'][i])+"_tesseract"
            if(name in label_dict):
                label_dict[name].append([x, y, x+w, y+h])
            else:
                label_dict[name] = [[x, y, x+w, y+h]]
    
    json_str = json.dumps(label_dict)
    print(label_dict)
            
    print("len of anno = ", label_dict.__len__())
    return json_str