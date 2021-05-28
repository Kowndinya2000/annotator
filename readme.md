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
### ```</>``` Open a ```terminal``` in the ```root_directory```
````
python3 setup.py  
````
---
## Managing dependencies
### ```</>``` Open a ```terminal``` in the ```root_directory```
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

### ```1.``` Run the ```bash script``` in the  ```root_directory```
````
chmod +x bash.sh
./bash.sh
````
### ```2.``` Open browser, enter ```http://0.0.0.0:7700``` 