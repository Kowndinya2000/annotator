import collections
import torch
import matplotlib.pyplot as plt
import numpy as np
import numpy
from cv2 import cv2
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
import dns
import pymongo
from coordinates import *
from config import root_directory
MongoConnection = pymongo.MongoClient('localhost',27017)


def create_training_data_images(distinct_annotations,user,directory_name):
  width_avg = 0
  height_avg = 0  
  database = MongoConnection.get_database("test_database")
  collections = database.list_collection_names()
  image_size = {}
  average_length = {}
  average_width = {}
  count = {}
  for distinct_name in distinct_annotations:
      average_length[distinct_name] = 0
      average_width[distinct_name] = 0
      count[distinct_name] = 0
      image_size[distinct_name] = {}
      for collection in collections:
        if( user in collection):
          image_name = collection.split("/")[1]
          image_size[distinct_name][image_name] = []

  document_count = 0 
  for distinct_name in distinct_annotations:
    for collection in collections:
      if( user in collection):
        query = {"name":distinct_name,"deleted":"0"}
        if( user in collection):     
          image_name = collection.split("/")[1]
          lis = database[collection].find(query)
          if(bool(lis)):
            for x in lis:
              x1 = min(int(x["polygon"]["pointlist"][0]['x']),int(x["polygon"]["pointlist"][1]['x']),int(x["polygon"]["pointlist"][2]['x']),int(x["polygon"]["pointlist"][3]['x']))
              x2 = max(int(x["polygon"]["pointlist"][0]['x']),int(x["polygon"]["pointlist"][1]['x']),int(x["polygon"]["pointlist"][2]['x']),int(x["polygon"]["pointlist"][3]['x']))
              y1 = min(int(x["polygon"]["pointlist"][0]['y']),int(x["polygon"]["pointlist"][1]['y']),int(x["polygon"]["pointlist"][2]['y']),int(x["polygon"]["pointlist"][3]['y']))
              y2 = max(int(x["polygon"]["pointlist"][0]['y']),int(x["polygon"]["pointlist"][1]['y']),int(x["polygon"]["pointlist"][2]['y']),int(x["polygon"]["pointlist"][3]['y']))
              im = np.array(Image.open(directory_name+"/data" +"/"+image_name))
              if(x1 > x2):
                tmp = x1
                x1 = x2
                x2 = tmp
              if(y1 > y2):
                tmp = y1
                y1 = y2
                y2 = tmp
              if(x1 < 0):
                x1 = 0
              if(x2 < 0):
                x2 = 0
              if(y1 < 0):
                y1 = 0
              if(y2 < 0):
                y2 = 0
              im_trim = im[y1:y2, x1:x2]
              count[distinct_name] += 1
              Image.fromarray(im_trim).save(directory_name + "/pre-process-trim" + "/" + distinct_name +'_trim' + str(count[distinct_name]) + '_'+ image_name)
              im = np.array(Image.open(directory_name + "/pre-process-trim"+ "/" + distinct_name +'_trim' + str(count[distinct_name]) + '_'+ image_name).convert('L'))
              gr_im = Image.fromarray(im).save(directory_name + "/pre-process-grey"+ "/" + distinct_name +'_grey' + str(count[distinct_name]) + '_'+ image_name)
              load_img_rz = np.array(Image.open(directory_name + "/pre-process-grey"+ "/" + distinct_name +'_grey' + str(count[distinct_name]) + '_'+ image_name))
              image_size[distinct_name][image_name].append(load_img_rz.shape)
              average_length[distinct_name] += load_img_rz.shape[0]
              average_width[distinct_name] += load_img_rz.shape[1]

  for distinct_name in distinct_annotations:
    if(count[distinct_name] > 0):
      average_length[distinct_name] = int(average_length[distinct_name]/count[distinct_name])
      average_width[distinct_name] = int(average_width[distinct_name]/count[distinct_name])

  main_tensor = []
  for files in os.listdir(directory_name+"/pre-process-grey"):
    if("grey" in files):
      for distinct_name in distinct_annotations:
        if(distinct_name in files):
          current_image = np.array(Image.open(os.path.join(directory_name+"/pre-process-grey",files)))
          resize_length = current_image.shape[0]
          resize_width = current_image.shape[1]
          abs_name = ""+os.path.join(directory_name+"/pre-process-grey",files)
          load_img_rz = cv2.imread(os.path.join(directory_name+"/pre-process-grey",files),cv2.IMREAD_UNCHANGED)
          width_avg = average_width[distinct_name]
          height_avg = average_length[distinct_name]
          resized = cv2.resize(load_img_rz,(average_width[distinct_name],average_length[distinct_name]),interpolation=cv2.INTER_AREA)  
          cv2.imwrite(abs_name.replace("_grey","_re").replace("/pre-process-grey","/processed"),resized)
  label_tensor = []
  total_count = 0
  for files in os.listdir(directory_name+"/processed"):
    if("_re" in files):
      flag = 0
      for t in range(len(distinct_annotations)):
        if(distinct_annotations[t]+"_" in files):
            data = np.array(Image.open(os.path.join(directory_name+"/processed",files)))
            main_tensor.append(data)
            label_tensor.append(np.array(distinct_annotations[t]))
            flag += 1
            total_count += 1

  dataset = []
  dataset.append(numpy.array(main_tensor))
  label_tensor = numpy.array(label_tensor)
  dataset.append(numpy.array(label_tensor))

  return [dataset,width_avg,height_avg]

def create_distinct_annotations(distinct_annotations,user,directory_name):

  return create_training_data_images(distinct_annotations,user,directory_name), distinct_annotations


def check_if_directory_exists(user):
    try:
        folders = os.listdir('/'.join(os.path.abspath(__file__).split("/")[:-1])+"/user-data")
        directory_name = os.path.join(root_directory,'model-building','user-data',user)
        if(user in folders):
            flush = os.popen('rm -rf '+directory_name).read()
            create_user_box = os.popen('mkdir '+directory_name).read()
            setup_directory = os.popen('cp -r '+os.path.join(root_directory,"lib","model_building","*")+ ' ' +directory_name+"/").read()
            return directory_name

        else:
            create_user_box = os.popen('mkdir '+directory_name).read()
            setup_directory = os.popen('cp -r '+os.path.join(root_directory,"lib","model_building","*")+' '+directory_name+"/").read()
            return directory_name
    except Exception as ex:
        print(ex)
        return "-1" 
def create_model_directory(user):
    try:
        print('try: ','/'.join(os.path.abspath(__file__).split("/")[:-1])+"/user-models")
        folders = os.listdir('/'.join(os.path.abspath(__file__).split("/")[:-1])+"/user-models")
        print('folders: ',folders)
        print('try2: ',root_directory,'model-building','user-models',user)
        directory_name = os.path.join(root_directory,'model-building','user-models',user)
        print('directory_name: ',directory_name)
        if(user in folders):
            return directory_name
        else:
            os.chdir("/home/iit/Desktop/kowndinya/annotator-web-tool")
            create_user_box = os.popen('mkdir '+directory_name).read()
            print(create_user_box)
            return directory_name
    except Exception as ex:
        print(ex)
        return "-1" 


def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                image[i][j] = 255
    return image


def create_dummy_image(height_of_image,width_of_image,character_height,character_width,character,probability,dataset):
    dummy_image = np.zeros((height_of_image,width_of_image))
    dummy_image = sp_noise(dummy_image,0.05)
    label_image = np.zeros((height_of_image,width_of_image))
    
    i = 5
    
    while i<height_of_image:
        j=5
        while j<width_of_image:
            prob = random.uniform(0,1)
            if(prob<=probability):
                number_of_images = dataset[character].shape[0]
                random_image_number = random.randint(0,number_of_images-1)
                sub_image = dataset[character][random_image_number]
                (thresh, sub_image) = cv2.threshold(sub_image, 127, 255, cv2.THRESH_BINARY)
                if(i+character_height<height_of_image and j+character_width < width_of_image):
                    dummy_image[i:i+character_height,j:j+character_width] = sub_image
                    label_image[i+(character_height//2),j+(character_width//2)]=199920 
            j+=character_width
            j+=2
            
        
        i+=character_height
        i+=5
        
    dummy_image[dummy_image<=127] = 0
    dummy_image[dummy_image>127] = 255
    return (dummy_image,label_image)


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

def make_dataset(class_label,dataset,no_of_images=100,probability=0.6):
    my_x = []
    my_y = []
    width_of_sub_region = np.array(dataset[class_label]).shape[-1]
    height_of_sub_region = np.array(dataset[class_label]).shape[-2]
    for i in range(no_of_images):
        image,label =  create_dummy_image(300,300,height_of_sub_region,width_of_sub_region,class_label,probability,dataset)
        my_x.append([image])
        my_y.append(label.reshape(1,-1))
    my_x = np.stack(my_x)
    my_y = np.vstack(my_y)
    my_x = torch.from_numpy(my_x)
    my_y = torch.from_numpy(my_y)
    return (my_x,my_y)

    
def train_model(train_loader1,train_loader2 = None,cuda = "cuda:0",kernel_height=30,kernel_width=30,max_epochs = 1):
    first_epoch_loss = None
    last_epoch_loss  = None

    device = torch.device(cuda if torch.cuda.is_available() else "cpu")
    net = cnn(kernel_height,kernel_width)
    if torch.cuda.device_count() > 1:
      print("Utilizing", torch.cuda.device_count(), "GPUs!")
      net = nn.DataParallel(net)
    net.to(device)
    loss_fn = nn.MSELoss()
    opt = optim.Adam(net.parameters(),lr=0.001)
    best_model = None
    min_loss=sys.maxsize

    for epoch in range(max_epochs):
        for i, data in enumerate(train_loader1, 0):
            my_X, my_Y = data
            my_X, my_Y = my_X.to(device), my_Y.to(device)
            opt.zero_grad()
            out = net(my_X)
            loss = loss_fn(out, my_Y)
            if(loss<min_loss):
                best_model = copy.deepcopy(net)
                min_loss = loss
            loss.backward()
            opt.step()
        
        print('Epoch: %d/%d' % (epoch, max_epochs),"loss: %d" %(loss))
        if(epoch == 0):
            first_epoch_loss = int(loss)
        elif(epoch == max_epochs-1):
            last_epoch_loss = int(loss)
    
    print("model trained")
    
    return (best_model,min_loss,first_epoch_loss,last_epoch_loss)


def lookup(annotation,user,document):
    directory_name = check_if_directory_exists(user)
    if(directory_name != "-1"):
        response,distinct_names_a = create_distinct_annotations([annotation],user,directory_name)
        training_dataset_a = response[0]
        data_dictionary = {}
        training_dataset_a[0] = 255-training_dataset_a[0]
        cv2.imwrite("test_sub_region.jpg",training_dataset_a[0][0])
        for x in range(len(training_dataset_a[1])):
          data_dictionary[training_dataset_a[1][x]] = []
        for x in range(len(training_dataset_a[1])):
          data_dictionary[training_dataset_a[1][x]].append(np.array(training_dataset_a[0][x]))
        

        from torch.utils import data
        while(True):
          width_of_sub_region = np.array(data_dictionary[annotation]).shape[-1]
          height_of_sub_region = np.array(data_dictionary[annotation]).shape[-2]
          label_map = {}
          count = 0
          label_list = []
          for y in training_dataset_a[1]:
            if(y in label_map.keys()):
              label_list.append(label_map[y])
            else:
              label_map.update({y:count})
              label_list.append(count)
              count += 1
          
          ims = []
        
          for x in training_dataset_a[0]:
            ims.append(np.array(x))
         
          lbls = []
          for x in training_dataset_a[1]:
            lbls.append(label_map[x])
          
          tensor = []
          tensor = [torch.tensor(ims),torch.tensor(lbls)]
          
          class_names = [x for x  in range(len(set(tensor[1].numpy())))]
      
          data_dictionary = {}
          for i in range(len(class_names)):
              data_dictionary[str(class_names[i])] = tensor[0][tensor[1] == i].numpy()
          from torch.utils import data
          (train_x,train_y) = make_dataset(class_label= '0',dataset = data_dictionary,no_of_images=100)
          
      
          cv2.imwrite("sample_train_document.jpg",train_x[0][0].numpy())
          train_x=train_x.type(torch.float32)
          train_y=train_y.type(torch.float32)
          train_dataset = data.TensorDataset(train_x,train_y)
          train_loader = data.DataLoader(train_dataset,batch_size=4 ,shuffle=True)
        

          kernel_height = height_of_sub_region
          kernel_width = width_of_sub_region


          if(kernel_height%2 == 0):
              kernel_height+=1
          if(kernel_width%2 == 0) :
              kernel_width+=1
              
        
       
          max_iter = 2
          true_learning = False
          while(max_iter > 0):
              max_iter = max_iter - 1
              best_model,loss,first_loss,last_loss = train_model(train_loader,max_epochs=20,kernel_height=kernel_height,kernel_width=kernel_width)
              if((first_loss*0.3) >= last_loss):
                  true_learning = True
                  break 
         
          print('loss=',int(loss))
          print('true_learning: ',true_learning)
          if(true_learning):
            print('inside true learning: ')
            if(create_model_directory(user) != "-1"):
                model_name= 'model_'+annotation+'.pth'
                print(model_name)
                torch.save(best_model.module.state_dict(),os.path.join(root_directory,'model-building','user-models',user,model_name))
                db = MongoConnection.get_database('models')
                collection = db['bounding_regions']
                annotation_name = user+"_"+annotation
                n_documents = collection.count_documents({'email':annotation_name})
                if(n_documents != 0):
                    collection.delete_one({'email':annotation_name}) 
                collection.insert_one({'email':annotation_name, 'boundary':str(kernel_height)+':'+str(kernel_width)})
                break
          else:
            print('model directory was nt created!')
            return "False"
          return "True"
    return "False"