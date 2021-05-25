import pytesseract
from pytesseract import Output
import numpy as np
from matplotlib import image
import os
import json

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
tessdata_dir_config = r'--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'


def get_annotations_data_tamil(im_path):
    print(im_path)

    img_path = im_path
    json_str = ''
    if(os.path.isfile(img_path)==False):
        print("not a valid image path")
    else: 
        img = image.imread(img_path)
    
    d = pytesseract.image_to_data(img, output_type=Output.DICT, config=tessdata_dir_config,lang="tam")
            
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