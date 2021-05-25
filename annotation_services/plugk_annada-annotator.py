# ----------------------------------------------------------------------
# This script is used to setup an annotation service for kannada language
# 
# @author: Kowndinya Boyalakuntla <cs17b032@iittp.ac.in>
# @date: 15/05/2021

#-----------------------------------------------------------------------
import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from config import root_directory
from plug_kannada import *


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(root_directory,'model-building','annotation-services-images-kannada')
def allowed_file(filename):
    ''' Checking wether the file has extension of type 'jpg'.
        Args:
        filename: 
                  Name of the file(image).
        Returns:
                  File name without extensions.
    '''
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/plug/tesseract-kannada', methods=['GET', 'POST'])
def upload_file():
    ''' Uploads the image into annoation-services-images-kannada
        and returns the annotations(json string) received.
    '''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print('**found file', file.filename)
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            print("*********__************")

            json_str = get_annotations_data_kannada(file_path)
            print("*********__************")
            return json_str
    return '''
    <!doctype html>
    <title>Model Prediction Server</title>
    <h1>Auto Annotation Service</h1>
    '''
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7005, debug=True)