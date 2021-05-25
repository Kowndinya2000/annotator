from pymongo import MongoClient
from xml.dom import minidom
import sys
import os
def prepare_auto_pool_template(user_email):
    try:
        connection = MongoClient('localhost',27017)
        print("connected Succesfully!!!")
        db = connection.get_database('models')
        collections= db["user_models"]
        for data in collections.find({"email":user_email}).limit(1):
          return data
    except Exception as e:
        print(e)
        return False
