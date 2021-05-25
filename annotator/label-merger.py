# -----------------------
# @author: Ramya Velaga
# @date: 27-05-2020
# ----------------------

#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------

import os
import cv2
from xml.dom import minidom
import sys
xml_files=os.listdir(r'Annotations/docs_user3%40gmail.com') 
print(xml_files)
number_keys=int(sys.argv[1]) 
key_list=[]
for n in range(number_keys):
    key_list.append(sys.argv[2+int(n)]) 
print(key_list)
if not os.path.exists('_'.join(key_list)):
    os.makedirs('_'.join(key_list)) 
    
for file in xml_files:
    mydoc = minidom.parse(os.path.join(r'Annotations/docs_user3%40gmail.com',file)) 
    image_name=mydoc.getElementsByTagName('filename')[0].childNodes[0].data 
    folder_name=mydoc.getElementsByTagName('folder')[0].childNodes[0].data
    img=cv2.imread(os.path.join('Images/'+folder_name,image_name))
    cv2.imshow('image',img)
    items = mydoc.getElementsByTagName('object')
    for element in items:
        element_list=element.getElementsByTagName('tag')
        tag_list=[]
        for a in element_list:
            tag_list.append(a.childNodes[0].data)
        print(tag_list)
        flag = 0
        if(all(x in tag_list for x in key_list)): 
            flag = 1
        x=element.getElementsByTagName('x')
        y=element.getElementsByTagName('y')
        start_x=int(x[0].childNodes[0].data)
        start_y=int(y[0].childNodes[0].data)
        end_x=int(x[2].childNodes[0].data)
        end_y=int(y[2].childNodes[0].data)
        print((start_x,start_y),(end_x,end_y))
        if(flag==1): 
            print(flag)
            img=cv2.rectangle(img,(start_x,start_y),(end_x,end_y),(100,150,0),2)
        else:
            img=cv2.rectangle(img,(start_x,start_y),(end_x,end_y),(255,0,0),1) 
    cv2.imwrite('_'.join(key_list)+'/'+image_name,img)
