from random import randint
from sklearn.feature_extraction import image
import cv2
import numpy as np
from PIL import Image
def create_patches(no_patches,path,a,b):
    im = np.array(Image.open(path).convert('L'))
    patches = image.extract_patches_2d(im, (a, b), max_patches=no_patches, random_state=randint(0,2**32-1))
    return patches
# create_patches(10,"/home/kowdinya/authentic-code/annotator-web-tool/lib/model_building/data/document3.jpg",34,96)
