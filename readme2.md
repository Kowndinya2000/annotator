<img src="logoupdated.png" width="200.75rem" height="128.25rem" align="right" />

# Akshara - Auto Annotation Platform [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)
> Auto annotation - Model Pooling - Plug n play Annotation Services 
----

## ```>``` Platform is available at: 
````
https://services.iittp.ac.in/annotator
````

## ```>``` Steps to setup Akshara
---
## Initial setup
### ```</>``` Open config.py in the folder ```annotator```
````
Set root_directory to the path of the folder where this repository is downloaded 
````
### ```</>``` Open config.py in the folder ```model-building```
````
Set root_directory to the path of the folder where this repository is downloaded 
````
### ```</>``` Open the file ```global_variables.pl``` in the folder ```annotator/static/perl```
```
Set $LM_HOME to path of the folder annotator
```
---
## Managing dependencies
### ```</>``` Open ```terminal``` in the ```root_folder```
````
pip install -r requirements.txt
````
---

## Setting up MongoDB

#### ```1.``` Install ```MongoDB shell``` in your linux machine ["https://docs.mongodb.com/manual/administration/install-on-linux/"]  
#### ```2.```  Type ```mongo``` on terminal and it should open the ```MongoDB shell``` on the terminal
#### ```3.``` Type the following commands to create ```databases``` and ```collections``` needed:
````
use test_database
db.createCollection('services_mapping')
use models
db.createCollection('bounding_regions')
db.createCollection('user_models')
use anno_admin
db.createCollection('author_job')
````
---

## Starting services

### ```1.``` Open ```2 terminals``` in the folder ```model-building```
````
python3 build-model.py
python3 auto-annotator.py
````

### ```2.``` Run the ```bash script``` in the folder ```annotator-web-tool```
````
chmod +x bash.sh
./bash.sh
````
### ```3.``` Open browser, enter ```http://0.0.0.0:5000``` 