#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 25/11/2020
#-----------------------------------------------------

from pymongo import MongoClient
import sys
import os
def update_author_job(user_email,doc_name):
    try:
        connection = MongoClient('localhost',27017)
        print("connected Succesfully!!!")
        db = connection.get_database('anno_admin')
        collections = db.list_collection_names()
        print(collections)
        if("author_job" in collections):
            query = {"email" : user_email}
            document = db["author_job"].find(query)[0]
            new_job_list = document["jobs"].replace(doc_name+":pending",doc_name+":complete")
            query1 = {"jobs" : document["jobs"]}
            query2 = { "$set" : {"jobs" : new_job_list }}
            db["author_job"].update_one(query1,query2)
            return True
    except Exception as e:
        print(e)
        return False        
