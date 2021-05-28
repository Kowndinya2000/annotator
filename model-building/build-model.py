import os
from flask import Flask, request
from pymongo import MongoClient
from model_api import *
from lookup import *
from time import sleep 
from config import root_directory
app = Flask(__name__)



#----------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#----------------------------------------------
#this route is to build a model and establishing connection with database
#and storing data of the models in database

@app.route('/build/<document>', methods=['GET', 'POST'])
def build_a_model(document):
    if request.method == 'POST':
        print('request reached server!')
        arguments = request.data.decode("utf-8").split(",")
        annotation = arguments[0]
        user = arguments[1]
        json_str = lookup(annotation,user,document)
        print(json_str)
        sleep(3)
        model_path=os.path.join(root_directory,'model-building','user-models',user)
        sleep(3)
        models_list = os.listdir(model_path)
        model_pool = ""
        for x in models_list:
            model_pool += x.replace("model_","").replace(".pth","")+"," 
        model_pool = model_pool[:len(model_pool)-1]
        try:
            connection = MongoClient('localhost',27017)
            print("connected Succesfully!!!")
            db = connection.get_database('models')
            collections = db.list_collection_names()
            print(collections)
            collections= db["user_models"]
            data = {}
            for old_data in collections.find({"email":user}).limit(1):
                data = old_data 
                print('data: ',data)
                update = False
                print('keys: ',data.keys())
                data["Pool_Closure"] = model_pool
                collections.delete_one({"email":user})
                collections.insert(data)
                return "true,"+model_pool
        except Exception as e:
            print(e)
            return "false,"+model_pool
    return '''
    <!doctype html>
    <title>ANNO MODEL SERVER</title>
    <h1>Model building server</h1>
    '''


#----------------------------------------------
# @author: DANDE TEJA         <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#----------------------------------------------
#Starting function to start the connection on the port 7003 and running on 
# the ip 0.0.0.0 

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5002, debug=True)