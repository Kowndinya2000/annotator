'''This script contains all the URL mappings of the flask app.

The URLs corresponding to the LabelMe tool are all mapped 
to the functions in this script.

For example,
    @main.route('/annotate'): maps the urls starting with '/annotate'
'''
#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------

from time import sleep
from pymongo import MongoClient
from flask import Blueprint, render_template, request, flash, jsonify, make_response,redirect,url_for,request
from flask import send_from_directory, Response, Markup
from flask_login import login_required, current_user
from . import db, create_app
import os,os.path, subprocess
import json
import xml.etree.ElementTree as xml
from .fetch_image_mod import *
import requests
from .pre_lookup import is_model_needed
connection = MongoClient('localhost',27017)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   
MEDIA_FOLDER = 'Images'


main = Blueprint('main', __name__)

i=0
#----------------------------------------------
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#----------------------------------------------
@main.route('/home')
def home():
    return render_template('home.html')
@main.route('/doanno',methods = ['POST'])
@login_required
def doanno():
    from .prepare_auto import prepare_auto_pool_template
    model_data = prepare_auto_pool_template(current_user.name)
    if(model_data != False):
        resp_data = {}
        resp_data.update({"Pool_Closure":model_data["Pool_Closure"]})
        for y in model_data:
            if(y != "_id" and y != "Pool_Closure" and y != "email"):
                resp_data.update({y:model_data[y]})
        print(resp_data)
        return resp_data
    else:
        return "False"
@main.route('/')
def index():
    return render_template('index.html')
@main.route('/logged_out')
def logged_out():
    return render_template('index-logout.html')
@main.route('/connect')
@login_required
def load_jobs():
    return render_template('load_jobs.html')
@main.route('/load')
@login_required
def load_profile():
    return render_template('profile.html', name=current_user.name)
#----------------------------------------------
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#----------------------------------------------
@main.route('/profile')
@login_required
def profile():
     ''' Renders the profile window after user clicks 'profile'
        or when user log in
    '''
    from .pending_jobs import generate_template
    if(generate_template(current_user.name, os.getcwd()+ '/' + __name__.replace(".main","")+"/templates/profile.html")):
        return render_template('profile.html', name=current_user.name)
    else:
        return render_template('no_job.html', name=current_user.name)


@main.route('/complete',methods = ['GET'])
@login_required
def done():
    doc_name = request.args.get("image")
    user_email = current_user.name
    try:
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
            return redirect(url_for('main.load_job')) 
    except Exception as e:
        print(e)
   

#route to upload the code    
@main.route('/upload')
@login_required
def upload():
    import os
    print(os.getcwd()+ '/' + __name__.replace(".main","")+"/Images/docs_"+current_user.name)
    from .images_exist import check_if_images_exist
    print(check_if_images_exist(os.getcwd()+ '/' + __name__.replace(".main","")+"/Images/docs_"+current_user.name, current_user.name))
    result = check_if_images_exist(os.getcwd()+ '/' + __name__.replace(".main","")+"/Images/docs_"+current_user.name, current_user.name)
    if(result[0]):
        return redirect(url_for('main.annotate', collection='LabelMe'+current_user.name, mode='i', 
                            folder='docs_'+current_user.name, image=result[1] ,username=current_user.name))
    else:
        mesg = "Please Upload an image first to annotate!"
        return render_template('upload.html', msg=mesg)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 27/04/2020
#----------------------------------------------
#route to annotate the image
@main.route('/annotate')
@login_required
def annotate():
  '''Renders drawing window after user clicks 'annotate'.

    This function takes image details as arguments and renders the drawing window.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user. 
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        image: Name of the image.

    Returns:
        Renders template for annotate window.
    '''
    collection = request.args.get('collection')
    mode = request.args.get('mode')
    folder_name = request.args.get('folder')
    image = request.args.get('image')
    return render_template('NewAnnotate.html', mimetype="text/html",collection=collection,mode=mode,folder=folder_name,image_name=image,user_id=current_user.name)

@main.route('/get_existing_models',methods = ['POST','GET'])
@login_required
def get_existing_models():
    if request.data:
        try:
            db = connection.get_database('models')
            collections= db["user_models"]
            for data in collections.find({"email":current_user.name}).limit(1):
                response_string = data["Pool_Closure"]
                print(response_string)
                if(response_string == ""):
                    return "false"
                else:
                    return response_string
        except Exception as e:
            print(e)
            return "false"
    return "false"    


#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/Images/<foldername>/<filename>', methods = ['GET'])
@main.route('/Images/<foldername>/<filename>', methods = ['GET'])
@login_required
def updateImage(foldername, filename):
    print("\n*****************\n")
    print('main-check-image-path: \n')
    final_image_path = MEDIA_FOLDER + "/" + foldername
    if("@" in final_image_path):
        final_image_path = final_image_path
    print(final_image_path)
    print("\n*****************\n")
    return send_from_directory(final_image_path, filename, as_attachment=True)
'''Sends requested image from directory.

    Request Arguments:
        foldername: Folder name.
        filename: Name of the image.

    Returns:
        Returns requested image retrieved from corresponding location.
    '''
#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/Annotations/<foldername>/<filename>', methods = ['GET'])
@login_required
def updateXMLforImg(foldername, filename):
    print("\n*****************\n")
    print('main-check-annotation-path: \n')
    final_image_path = "Annotations"+"/"+foldername
    final_image_path = "Annotations"+"/"+foldername
    print(final_image_path)
    print("\n*****************\n")
    path_anno = r"Annotations/"+foldername
    path_anno = path_anno.replace("@",'%40')
    print(path_anno)
    return send_from_directory(path_anno, filename, as_attachment=True, cache_timeout=0)

@main.route('/AnnotationCache/<foldername>/<filename>', methods = ['GET'])
@login_required
def updateXMLTemplate(foldername, filename):
   '''Sends XML template for annotations.

    Request Arguments:
        foldername: Folder name.
        filename: Name of the image.

    Returns:
        Sends the XML template.
    '''
    path_anno = r"AnnotationCache/"+foldername
    path_anno = path_anno
    return send_from_directory(path_anno, filename, as_attachment=True)

@main.route('/wait_loader')
@login_required
def wait_loader():
    image = request.args.get('image')
    return redirect(url_for('main.annotate', collection='LabelMe'+current_user.name, mode='i', 
                            folder='docs_'+current_user.name, image=image,username=current_user.name))    

@main.route('/train', methods = ['POST','GET'])
@login_required
def trainMODEL():
    if request.data:
        doc = request.args.get('document')
        annotation = request.data.decode('utf-8')
        print('annotation: ',annotation)
        user_id = current_user.name
        if(is_model_needed(annotation,user_id,1)):
            request_data = annotation + "," + user_id
            try:
                r = requests.post('http://0.0.0.0:7002/build/'+doc,data=request_data)
                return_response = r.text
                print('---------------')
                print(return_response)
                print('---------------')
                if("true," in return_response):
                    return return_response
                else:
                    return "false,-1"
            except Exception as ex:
                print(ex)
                return "false,-1"
        else:
            print('Model cannot be built at this moment')
    return "false,-1"
@main.route('/wdb_loader')
@login_required
def wdb_loader():
    annotation = str(request.args.get('ann'))
    im = (request.args.get('im'))
    print('annotation: ',annotation)
    print('im: ',im)
    fp = open(os.getcwd()+"/annotator/templates/wdb-loader.html",'w')
    fp.write(''' 
                <!DOCTYPE html>
                <html lang="en" >
                <head>
                <meta charset="UTF-8">
                <title>Check if Model can be built?</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
                <link rel="stylesheet" href="/annotator/static/css/wdb-loader.css">
                </head>
                <body>
                    <a href="/annotator/train?ann=''' + annotation + '''&im=''' + im + '''" style="display: none;" id="nexts">Next</a>
                        <script>
                        setTimeout(() => {
                            document.getElementById('nexts').click()
                        }, 200);
                    </script>
                <div class="loader"></div>
                <h1 style="color: #fff;position: absolute;bottom: 8rem;">Checking if models can be built at this moment?</h1>
                </body>
                </html>
        ''')
    fp.close()
    return render_template('wdb-loader.html',mimetype="text/html")


#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 03/05/2020
#----------------------------------------------
@main.route('/static/perl/submit.cgi', methods = ['POST','GET'])
@login_required
def writeToXML():
    '''Invokes submit.cgi script.

    This function runs submit.cgi script to write the XML data to the corresponding file.
    '''
    filepath = os.path.join(APP_ROOT, "static", "perl","submit.cgi")
    if request.data:
        print('inside loop')
        msg = request.data
        pipe = subprocess.Popen(["perl", filepath], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        import xml.etree.ElementTree as ET
        root=ET.fromstring(msg)
        root[1].text =   "docs_" + current_user.name
        xmlstr = ET.tostring(root, encoding='unicode', method='xml')
        msg_bytes = str.encode(xmlstr)
        pipe.stdin.write(msg_bytes)
        pipe.stdin.close()
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
        print(root[0].text)
        print(filepath)
        from .wdb import writeToDB
        resp = writeToDB(os.getcwd()+ '/' + __name__.replace(".main","")+"/Annotations/docs_"+current_user.name+"/"+root[0].text.replace(".jpg",".xml"))
        print(resp)
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
    return ""
@main.route('/add/services/static/perl/submit.cgi/<service_url>', methods = ['POST','GET'])
@login_required
def writeToXMLAndAddService(service_url):
    filepath = os.path.join(APP_ROOT, "static", "perl","submit.cgi")
    if request.data:
        print('inside loop')
        msg = request.data
        pipe = subprocess.Popen(["perl", filepath], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        import xml.etree.ElementTree as ET
        root=ET.fromstring(msg)
        root[1].text =   "docs_" + current_user.name
        xmlstr = ET.tostring(root, encoding='unicode', method='xml')
        msg_bytes = str.encode(xmlstr)
        pipe.stdin.write(msg_bytes)
        pipe.stdin.close()
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
        print(root[0].text)
        print(filepath)
        from .wdb import writeToDB
        resp = writeToDB(os.getcwd()+ '/' + __name__.replace(".main","")+"/Annotations/docs_"+current_user.name+"/"+root[0].text.replace(".jpg",".xml"))
        print(resp)
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
        if(".jpg" in root[0].text):
            image_name = root[0].text.replace(".jpg","")
        collection_name = "docs_"+ current_user.name + "/" + image_name + "/english"
        if("\n" in collection_name):
            collection_name = collection_name.replace("\n","")
        print("teseeract: collection- ",collection_name)
        db = connection.get_database('test_database')
        collection = db["services_mapping"]
        for old_data in collection.find({"collection_name":"services_list"}).limit(1):
            data = old_data 
            print('data: ',data)
            update = False
            print('keys: ',data.keys())
            for key in data.keys():
                print('key: ',key," , pool_name: ",collection_name)
                if(key == collection_name):
                    update = True
                    break 
                print('update: ',update)
                break 
            collection.delete_one({"collection_name":"services_list"})
            if(update):
                update_service_url = service_url.replace(",","/")
                onDeduplication = list(set((data[collection_name] + "^" + update_service_url).split("^")))
                updateStr = ",".join(onDeduplication)
                data[collection_name] = updateStr
            else:
                data.update({collection_name: service_url})
            print('final: ',data)
            collection.insert(data) 
            break
    return ""
@main.route('/add/services/<image_name>/<service_url>', methods = ['POST','GET'])
@login_required
def addServices(image_name, service_url):
    collection_name = "docs_"+ current_user + "/" + image_name + "/english"
    db = connection.get_database('test_database')
    collection = db["services_mapping"]
    for old_data in collection.find({"collection_name":"services_list"}).limit(1):
        data = old_data 
        print('data: ',data)
        update = False
        print('keys: ',data.keys())
        for key in data.keys():
            print('key: ',key," , pool_name: ",collection_name)
            if(key == collection_name):
                update = True
                break 
            print('update: ',update)
            break 
        collection.delete_one({"collection_name":"services_list"})
        if(update):
            onDeduplication = list(set((data[collection_name] + ":" + service_url).split(":")))
            updateStr = ",".join(onDeduplication)
            data[collection_name] = updateStr
        else:
            data.update({data[collection_name]: service_url})
        print('final: ',data)
        collection.insert(data) 
        return "true"
    return "false"



@main.route('/annotate_reload')
@login_required
def reload_annotation():
    model = request.args.get("model")
    visibility = request.args.get("visibility")
    display = request.args.get("display")
    print(model)
    print(visibility)
    print(display)
    return render_template("NewAnnotate.html",mimetype="text/html", model=model, visibility=visibility, display="visible")
    
@main.route('/add',methods=['POST'])
@login_required
def get_value():
    global i
    app = create_app()
    image=request.form['image']
    print(image)
    json_dir = app.config['UPLOAD FOLDER'].replace('img','json')
    image_dir = os.path.join(json_dir,str(image))+'.json'
    print(image_dir)
    with open(image_dir,'w') as f:
      json.dump(request.form.to_dict(flat=False),f)
    i+=1
    return jsonify(success=True)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 26/04/2020
#----------------------------------------------
@main.route('/static/perl/write_logfile.cgi', methods=['POST'])
@login_required
def write_log():
    '''Invokes write_logfile.cgi script.

    This function runs write_logfile.cgi script to write to the logfile.
    '''
    filepath = os.path.join(APP_ROOT, "static", "perl","write_logfile.cgi")
    if request.data:
        msg = request.data
        pipe = subprocess.Popen(["perl", filepath], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        pipe.stdin.write(msg)
        pipe.stdin.close()
    return ""

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/static/perl/fetch_image.cgi', methods=['GET'])
@login_required
def fetch_image():
    '''Fetches details of teh next image for the tool.

    This function takes image details as arguments and returns the details 
    for the next image to be rendered on the window for annotation.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user. 
        collection: Name of collection that current image belongs to.
        folder: Folder name.
        im_name: Name of the image.

    Returns:
        Returns foldername and the name of the image file in the form of an xml string.
    '''
    mode = request.args.get('mode')
    useremail = request.args.get('username')
    collection = request.args.get('collection')
    folder = request.args.get('folder')
    im_name = request.args.get('im_name')

    dir,file = get_data(APP_ROOT, mode, useremail, collection, folder, im_name)
    xml_str = "<out><dir>"+ dir + "</dir><file>"+ file+"</file></out>"
    return Response(xml_str, mimetype='text/xml')

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 21/05/2020
#----------------------------------------------


@main.route('/annotate/auto/model', methods=['GET'])
@login_required
def fetch_model_annotations():
    '''Returns annotations generated by Tesseract OCR.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user requesting auto annotation. 
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        image: Name of the image.

    Returns:
        Returns a json string containing image annotations.
    '''
    pool_name = request.args.get('pool')
    print('pool_name',pool_name)
    if(pool_name != ""):
        mode = request.args.get('mode')
        useremail = request.args.get('username')
        collection = request.args.get('collection')
        folder = request.args.get('folder')
        im_name = request.args.get('image')
        print(collection, mode, useremail, folder, im_name)
        #sleep(2)
        url_server = "http://0.0.0.0:7001/predict/"+pool_name + "/" + useremail
        image_path = os.getcwd()+ '/' + __name__.replace(".main","")+"/Images/"+folder+"/"+im_name
        fin = open(image_path, 'rb')
        files = {'file': fin}
        try:
            
            r = requests.post(url_server, files=files)
            print(r.text)
            return Response(r.text)
        finally:
            fin.close()
    return json.loads("{}")
@main.route('/annotate/auto/tesseract', methods=['GET'])
@login_required
def fetch_auto_annotations():
    '''Returns annotations generated by Tesseract OCR.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user requesting auto annotation. 
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        image: Name of the image.

    Returns:
        Returns a json string containing image annotations.
    '''
    mode = request.args.get('mode')
    username = request.args.get('username')
    collection = request.args.get('collection')
    folder = request.args.get('folder')
    im_name = request.args.get('image')
    url_server = request.args.get('service')
    print(collection, mode, username, folder, im_name, url_server)

    
    image_path = os.getcwd()+ '/' + __name__.replace(".main","")+"/Images/"+folder+"/"+im_name
    fin = open(image_path, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(url_server, files=files)
        print(r.text)
        return Response(r.text)
    finally:
        fin.close()

@main.route('/pool_creation', methods=['POST'])
@login_required
def pool_creation():
    pool_name = request.args.get('key')
    print('pool_name',pool_name)
    if(pool_name != ""):
        print("Inside pool creation")
        val = request.args.get('val')
        if(val[len(val)-1] == ","):
            val = val[:len(val)-1]
        print('val: ',val)
        db = connection.get_database('models')
        collections = db.list_collection_names()
        print(collections)
        collections= db["user_models"]
        data = {}
        for old_data in collections.find({"email":current_user.name}).limit(1):
            data = old_data 
            print('data: ',data)
            update = False
            print('keys: ',data.keys())
            for key in data.keys():
                print('key: ',key," , pool_name: ",pool_name)
                if(key == pool_name):
                    update = True
                    break 
            print('update: ',update)
            break 
        collections.delete_one({"email":current_user.name})
        if(update):
            data[pool_name] = val 
        else:
            data.update({pool_name: val})
        print('final: ',data)
        collections.insert(data)     
    return "failed"


