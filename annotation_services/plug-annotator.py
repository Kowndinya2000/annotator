import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from config import root_directory
from plug import *


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(root_directory,'model-building','annotation-service-images')
def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/plug/tesseract', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print('**found file', file.filename)
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            print("*********__************")
    
            #getting annotations
            json_str = get_annotations_data(file_path)
            print("*********__************")
            return json_str
    return '''
    <!doctype html>
    <title>Model Prediction Server</title>
    <h1>Auto Annotation Service</h1>
    '''
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7003, debug=True)