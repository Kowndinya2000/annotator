import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import torch.nn as nn
from torch.utils import data
import torch.optim as optim
import sys
import copy
import random
from PIL import Image
import torchvision
import torchvision.transforms as transforms
import string
import matplotlib
from joblib import Parallel, delayed  
import multiprocessing
import pymongo

#establising connection with Mongodb database
MongoConnection = pymongo.MongoClient('localhost',27017)
print('ok connected!')
#geting models from the database
db = MongoConnection.get_database('models')
collection = db['bounding_regions']
directory_name = os.path.dirname(os.path.abspath(__file__)) 
print(directory_name)
 

#----------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#----------------------------------------------
#CNN model code for any subregion should pass through this function
class cnn(nn.Module):
    def __init__(self,height_of_sub_region,width_of_sub_region):
        super(cnn,self).__init__()
        self.cnn_model = nn.Sequential(
            nn.Conv2d(1,10,(height_of_sub_region,width_of_sub_region),padding=((height_of_sub_region-1)//2,(width_of_sub_region-1)//2)),
            nn.ReLU(),
            nn.Conv2d(10,1,1,padding=(0,0)),
            nn.ReLU(),    
        )
    def forward(self,x):
        x = self.cnn_model(x)
        x = x.view(x.size(0), -1)
        return x


def test_model(best_model,x,cuda = "cuda:0"):
    
    device = torch.device(cuda if torch.cuda.is_available() else "cpu") 
    best_model.to(device)
    test_x = [x]
    test_x = np.stack(test_x)
    test_x = torch.from_numpy(test_x)
    test_x=test_x.type(torch.float32)
    test_x = test_x.to(device)
    out = best_model(test_x)
    y_pred = out[0].detach().cpu().numpy()
    y_pred = y_pred.reshape(x.shape[1],x.shape[2])
    y_pred = y_pred/np.max(y_pred)
    y_pred = y_pred*255
    y_pred[y_pred<0] = 0
    y_pred = y_pred.astype(np.uint8)
    return y_pred



#gpu compatable code for running the models 
def annotate_gpu(image,user,model_pool):
    image_copy = copy.deepcopy(image)
    height_of_image = image.shape[0]
    width_of_image = image.shape[1]
    image = image.reshape((1,image.shape[0],image.shape[1]))
    device = torch.device("cuda:0")
    user_id  = user
    model_names = os.listdir(os.path.join(directory_name,'user-models/',user_id))
    print(os.path.join(directory_name,'user-models/',user))
    print(model_names)
    if("," not in model_pool):
        models_requested = [model_pool]
    else:
        models_requested = model_pool.split(",")
    names = []
    for mod in models_requested:
        print('**',mod)
        for name in model_names:
            if(name == "model_"+mod+".pth"):
                names.append(name)
    print('--------------')
    print(names)
    print('--------------')
    model_names = names
    print(model_names)
    result = []
    

    
    for name in model_names:
        print(user_id+"_"+name.replace('model_','').replace('.pth',''))
        for y in collection.find({'email':user_id+"_"+name.replace('model_','').replace('.pth','')}).limit(1):
            print('inside loop')
            print(y)
            z= y['boundary'].split(':')     
            print('z: ',z) 
            model = cnn(int(z[0]),int(z[1]))
            model.load_state_dict(torch.load(os.path.join(directory_name,'user-models',user_id,name)))
            pred = test_model(model,image,device)
            bounding_boxes = find_bounding_boxes(pred,int(z[0]),int(z[1]))
            for result_annotation in bounding_boxes:
                top_x=int(result_annotation[1])
                top_y=int(result_annotation[2])
                bottom_x=int(result_annotation[3])
                bottom_y=int(result_annotation[4])
                confidence=int(result_annotation[0])
                annotation = [name[6:-4],confidence,top_x,top_y,bottom_x,bottom_y]
                result.append(annotation)
                color =(0,255,0)
                thickness=1
                image_copy = cv2.rectangle(image_copy, (top_x,top_y), (bottom_x,bottom_y), color, thickness)
                  
    return result,image_copy

         
# preporcessing of the image before building the model
def preprocess_img(img):
    mod_img = copy.deepcopy(img)
    ht, wd, cr = img.shape[0], img.shape[1], img.shape[2]
    for i in range(ht):
        for j in range(wd):
            for k in range(cr):
                if(255-mod_img.item(i, j, k)<0):
                    mod_img.itemset((i, j, k), 0)
                else:
                    mod_img.itemset((i, j, k), 255-img.item(i, j, k))

    return mod_img



 #annotating the iamge document
def annotate(image,user,pool_name):
    image_copy = copy.deepcopy(image)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = 255-image
    image[image<127] = 0
    image[image>=127] = 255
    cv2.imwrite('test.jpg',image)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    if(torch.cuda.is_available()):
        print("working on gpu")
        return annotate_gpu(image,user,pool_name)
    

#finding bounding boxes for the image depending upon the subregion models 
#selected for annotation
def find_bounding_boxes(label,height_of_sub_region,width_of_sub_region):
    bounding_boxes = []
    label = label/np.max(label)
    image_height = label.shape[-2]
    image_width = label.shape[-1]
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if(label[i][j]>= 0.5):
                bounding_boxes.append([label[i][j],max(0,j-(width_of_sub_region//2)),max(0,i-(height_of_sub_region//2)),min(image_width,j+(width_of_sub_region//2)),min(image_height,i+(height_of_sub_region//2))])
    
    return bounding_boxes