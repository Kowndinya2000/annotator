#----------------------------------------------
# @author: Vijay Chilaka <cs17b008@iittp.ac.in>
# @date: 22/01/2021
#----------------------------------------------
import dns
import pymongo
def is_model_needed(annotation,user,threshold):
    ''' Checks if model should be built based on the threshold. 
    Threshold here refers to number of images needed to build a model (as specified by user). ''' 
    print("********inside is_model_needed*******")
    MongoConnection = pymongo.MongoClient('localhost',27017)
    database = MongoConnection.get_database("test_database")
    collections = database.list_collection_names()
    print(collections)
    count = 0
    for collection in collections:
        if(count >= 1):
            return True
        else:
            if(user in collection):
                anno_info = database[collection].find({"name":annotation})
                for x in anno_info:
                    count += 1
                if(count >= 1):
                    return True
    print(count)
    print("**************************")
    return False
