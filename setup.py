import os 
from sys import platform
rootDir = os.getcwd() 
if(platform == "win32"):
    rootDir = rootDir.replace("\\","\\\\")
    fp = open(rootDir+"\\annotator\config.py",'w')
    fp.write('''root_directory = "''' + rootDir + '''"''')
    fp.close()
    fp = open(rootDir+"\\model-building\config.py",'w')
    fp.write('''root_directory = "''' + rootDir + '''"''')
    fp.close()
    fp = open(rootDir+"\\annotator\static\perl\globalvariables.pl",'w')
    fp.write('''#!/usr/bin/perl
    $LM_HOME = "''' + rootDir + '''\\\\annotator";''')
    fp.close()
    fp = open(rootDir+"\\annotation_services\config.py",'w')
    fp.write('''root_directory = "''' + rootDir + '''\\\\annotation_services"''')
    fp.close()
    fp = open(rootDir+"\\bash.sh",'w')
    fp.write("")
    fp.close()
    fp = open(rootDir+"\\bash.sh",'a')
    fp.write("python3 setup.py\n")
    fp.write("export FLASK_ENV=development\nexport FLASK_APP=annotator\n")
    fp.write("flask run --host=0.0.0.0 --port=4000 &\n")
    fp.write("python3 "+'''"'''+rootDir+'''\\\\model-building\\\\auto-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''\\\\model-building\\\\build-model.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''\\\\annotation_services\\\\plugk_annada-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''\\\\annotation_services\\\\plug-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''\\\\annotation_services\\\\plug_telugu-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''\\\\annotation_services\\\\plug_tamil-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''\\\\annotation_services\\\\plug_Malayalam-annotator.py"\n''')
    fp.close()

else:
    fp = open(rootDir+"/annotator/config.py",'w')
    fp.write('''root_directory = "''' + rootDir + '''"''')
    fp.close()
    fp = open(rootDir+"/model-building/config.py",'w')
    fp.write('''root_directory = "''' + rootDir + '''"''')
    fp.close()
    fp = open(rootDir+"/annotator/static/perl/globalvariables.pl",'w')
    fp.write('''#!/usr/bin/perl
    $LM_HOME = "''' + rootDir + '''/annotator";''')
    fp.close()
    fp = open(rootDir+"/annotation_services/config.py",'w')
    fp.write('''root_directory = "''' + rootDir + '''/annotation_services"''')
    fp.close()
    fp = open(rootDir+"/bash.sh",'w')
    fp.write("")
    fp.close()
    fp = open(rootDir+"/bash.sh",'a')
    fp.write("python3 setup.py\n")
    fp.write("export FLASK_ENV=development\nexport FLASK_APP=annotator\n")
    fp.write("flask run --host=0.0.0.0 --port=4000 &\n")
    fp.write("python3 "+'''"'''+rootDir+'''/model-building/auto-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''/model-building/build-model.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''/annotation_services/plugk_annada-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''/annotation_services/plug-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''/annotation_services/plug_telugu-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''/annotation_services/plug_tamil-annotator.py" &\n''')
    fp.write("python3 "+'''"'''+rootDir+'''/annotation_services/plug_Malayalam-annotator.py"\n''')
    fp.close()
