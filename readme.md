Steps to run the tool 

1. Open config.py in the folder ```annotator```
````
Change the value of the variable root_directory to the path of the folder where this repository is downloaded 
````
2. Open config.py in the folder ```model-building```
````
Change the value of the variable root_directory to the path of the folder where this repository is downloaded 
````
3. Open the file ```global_variables.pl``` in the folder ```annotator/static/perl```
```
Change the value of the variable ```$LM_HOME`` to path of the folder ```annotator```
```
4. Run the two files ```build-annotator.py``` and ```auto-annotator.py``` inside the folder ```model-building``` on two seperate terminals
```
python3 build-model.py
python3 auto-annotator.py
```
5. Finally run the file  ```bash.sh``` (present in the root directory of this repository)
```
chmod +x bash.sh
./bash.sh
```
6. Open browser, enter ```http://0.0.0.0:7000``` and use the tool.
