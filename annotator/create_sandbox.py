#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------

import os
from .config import root_directory


#sandbox creation code
def create_sandbox(user):
    try:
        path = os.getcwd() + "/annotator"
        if("docs_"+user in os.listdir(path+"/Images/")):
            flush = os.popen('rm -rf' + " " + path + "/Images/docs_"+user).read()
            print(flush)
            print('Deleted old documents')
        create = os.popen('mkdir '+path+"/Images/docs_"+user).read()
        print(create)
        print('Sandbox ready!')
        copy_docs = os.popen('cp -r '+os.path.join(root_directory,"lib","model_building","data","*")+" "+path + "/Images/docs_"+user).read()
        print(copy_docs)
        print('Documents created for the user successfully!')
        return True
    except Exception as ex:
        print(ex)
        return False


#user specific annotation stored directory code
def annotations_directory(user):
    try:
        path = os.getcwd() + "/annotator"
        if("docs_"+user in os.listdir(path+"/Annotations/")):
            flush = os.popen('rm -rf' + " " + path + "/Annotations/docs_"+user).read()
            print(flush)
            print('Deleted old annotations')
        create = os.popen('mkdir '+path+"/Annotations/docs_"+user).read()
        print(create)
        print('Annotation directory ready!')
        return True
    except Exception as ex:
        print(ex)
        return False




def dirlist(user):
    try:
        dir_user = user
        path = os.getcwd() + "/annotator"
        if("labelme"+dir_user+".txt" in os.listdir(path+"/AnnotationCache/DirLists/")):
            flush = os.popen('rm -rf' + " " + path + "/AnnotationCache/DirLists/labelme"+dir_user+".txt").read()
            print(flush)
            print('Deleted dir list')
        fp = open(path+"/AnnotationCache/DirLists/labelme"+dir_user+".txt",'a')
        documents = os.listdir(path + "/Images/docs_"+user)
        for names in documents:
            fp.write('docs_'+dir_user+","+names+"\n")
        fp.close()
        print('DirList ready!')
        return True,documents
    except Exception as ex:
        print(ex)
        return False,-1