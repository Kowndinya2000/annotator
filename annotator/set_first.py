#----------------------------------------------
# @author: Kowndinya Boyalakuntla <cs17b032@iittp.ac.in>
# @date: 25/11/2020
#----------------------------------------------
import sqlite3
import os
import sys

root = sys.argv[2]
emails = []
emails.append(sys.argv[1])
print(root)
conn = sqlite3.connect(root + 'db.sqlite')
cursor = conn.execute("SELECT * from user")


def set_template_xmls_ready(emails):
    ''' After user signs up, this function creates the user folder under annotation cache '''
    template_path = root+"/AnnotationCache/XMLTemplates/"
    for x in emails:
        cmd = "cp "+template_path+"docs.xml " + template_path + "docs_"+x+".xml"
        os.popen(cmd)
        cmd = "cp "+template_path+"labelme.xml " + template_path + "labelme_"+x+".xml"
        os.popen(cmd)
    print('templates have been set successfully!')


def set_annotation_path_ready(emails):
    ''' After user signs up, this function creates the user folder under annotations '''
    annotation_path = root+"/Annotations/"
    folders = os.listdir(annotation_path)
    folders_trim = []
    for y in folders:
        folders_trim.append(y.replace("docs_",""))
    diff = list(set(emails)-set(folders_trim))
    for x in diff:
        cmd = "mkdir "+ annotation_path + "docs_" + x 
        os.popen(cmd)
    print('annotation folders have been set successfully!')


def set_image_path_ready(emails):
    ''' After user signs up, this function creates the user folder under Images '''
    image_path = root+"/Images/"
    folders = os.listdir(image_path)
    folders_trim = []
    for y in folders:
        folders_trim.append(y.replace("docs_",""))
    diff = list(set(emails)-set(folders_trim))
    for x in diff:
        cmd = "mkdir "+ image_path + "docs_" + x 
        os.popen(cmd)
    print('image folders have been set successfully!')


def boot_setup():
   ''' This function calls the functions that create user sandbox folders '''
   set_template_xmls_ready(emails)
   set_annotation_path_ready(emails)
   set_image_path_ready(emails)