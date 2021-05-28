import os
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask import send_file
from config import root_directory


#allowed extension files are only accepeted on the service
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from model_api import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(root_directory,'model-building','user-images')
def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS





#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------
#route to pool the models specified by the user
#and uploading the predicted pools to a specific user
@app.route('/predict/<pool_name>/<user>', methods=['GET', 'POST'])
def upload_file_pronoun(pool_name,user):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print('**found file', file.filename)
            print(user)
            filename = secure_filename(file.filename)
            if(user in os.listdir(app.config['UPLOAD_FOLDER'])):
                clean = os.popen('rm -rf '+os.path.join(root_directory,'model-building','user-images',user,"*")).read()
                print(clean)
                print('cleaned')
            else:
                make = os.popen('mkdir '+os.path.join(root_directory,'model-building','user-images',user)).read()
                print(make)
                print('directory created!')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],user, filename))
            request_data = pool_name
            print('request-data: ',request_data)
            last = request_data[len(request_data)-1]
            if(last == ','):
                request_data = request_data[:len(request_data)-1]
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],user, filename)
            print(file_path)
            print("*********__************")
            json_str = get_model_data(user,file_path,request_data)
            print("*********__************")
            return json_str
    return '''
    <!doctype html>
    <title>Model Prediction Server</title>
    <h1>Auto Annotation Service</h1>
    '''




#----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#----------------------------------------------------
#main route running on port number 7001 and hosting on the
#IP address 0.0.0.0
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)