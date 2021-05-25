#----------------------------------------------
# @author: Vijay Chilaka <cs17b008@iittp.ac.in>
# @date: 25/11/2020
#----------------------------------------------
from time import sleep
def writeToDB(path):
    ''' This function writes the annotations from XML file to the database '''
    sleep(2)
    try:
        if("\n" in path):
            path = path.replace("\n","")
        xml_string = open(path,'r').read()
        resp = insert_function(xml_string)
        return [True,resp]
    except Exception as ex:
        print(ex)
        return [False,-1]
flag = False
def insert_function(msg):
    try:
        from pymongo import MongoClient
        import os
        import xml.etree.ElementTree as ET

        try:
            connection = MongoClient('localhost',27017)
            print("connected Succesfully!!!")
        except Exception as e:
            print(e)

       
        print(type(msg))

        root=ET.fromstring(msg)
        print("\n****",root,"*******\n")
        
        
        db = connection.get_database('test_database')
        print("\n****",root,"*******\n")
        fileName = root[0].text
        folderName = root[1].text
        path = folderName+"/"+fileName
        
        collection1 = db.main
        
        tablename = path +"/"+"english"
        drop_collection = db[tablename].drop()
        query = {"path":path}
        collection1.delete_one(query)
        
        
        collection2 = tablename
        object_count=0
        source = {}
        source["sourceImage"] = root[2][0].text
        source["sourceAnnotation"] = root[2][1].text
        child_index=0
        table_1 = {}
        objectlist = []
        for child in root:
        	if child.tag == "imagesize":
        		imagesize={}
        		imagesize["nrows"]=root[child_index][0].text
        		imagesize["ncols"]=root[child_index][1].text
        	if child.tag == "object":
        		object = {}
        		object["index"]=object_count
        		object["name"] = root[child_index][0].text
        		object["deleted"] = root[child_index][1].text
        		object["verified"] = root[child_index][2].text
        		object["occluded"] = root[child_index][3].text
        		taglist = []
        		for i in root[child_index][4]:
        			taglist.append(i.text)
        		object["taglist"] = taglist
        		hasparts=[]
        		ispartof=[]
        		for j in root[child_index][5]:
        			if j.tag=="hasparts" and j.text!=None:
        				for k in j.text:
        					if k != ",":
        						hasparts.append(k)
        			if j.tag=="ispartof" and j.text!=None:
        				for k in j.text:
        					if k != ",":
        						ispartof.append(k)
        		object["hasparts"]=hasparts
        		object["ispartof"]=ispartof
        		object["date"] = root[child_index][6].text
        		object["id"] = root[child_index][7].text
        		object["type"] = root[child_index][8].text
        		polygon = {}
        		pointlist = []
        		for i in root[child_index][9]:
        			if i.tag == "username":
        				polygon["username"] = i.text
        			if i.tag == "closed_date":
        				polygon["closed_date"] = i.text
        			pt = {}
        			if i.tag == "pt":
        				for j in i:
        					if j.tag == "x":
        						pt["x"] = j.text
        					if j.tag == "y":
        						pt["y"] = j.text
        					if j.tag == "time":
        						pt["time"] = j.text
        				pointlist.append(pt)
        		polygon["pointlist"] = pointlist
        		object["polygon"] = polygon
        		objectlist.append(object)
        		db[collection2].insert_one(object)
        		object_count = object_count+1
        	child_index = child_index + 1
        mainTable = {}
        mainTable["path"] = path
        mainTable["source"] = source
        mainTable["imagesize"] = imagesize
        print(mainTable,"_____________**********__________")
        collection1.insert_one(mainTable)
        flag = True
    except Exception as ex:
        print(ex)
        flag = False
    if(flag):
        return True
    else:
        return False
