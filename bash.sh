python3 setup.py
export FLASK_ENV=development
export FLASK_APP=annotator
flask run --host=0.0.0.0 --port=5000 &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\model-building\\auto-annotator.py" &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\model-building\\build-model.py" &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\annotation_services\\plugk_annada-annotator.py" &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\annotation_services\\plug-annotator.py" &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\annotation_services\\plug-telugu-annotator.py" &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\annotation_services\\plug-tamil-annotator.py" &&
python3 "C:\\BTP-Code Refactoring\\annotator-web-tool\\annotation_services\\plug-Malayalam-annotator.py"
