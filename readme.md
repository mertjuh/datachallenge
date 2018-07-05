# Group 1 datachallenge assignment


This repository contains the source code for the final poster. All the information that is displayed on the poster is gathered using the algorithms inside this project.
# Prerequisites (MongoDB)
To run this project, make sure an instance of mongodb is running. The download link is listed here https://www.mongodb.com/download-center#community. Choose the community Server edition and your desired operation system. Install using the default settings but also choose the option to add MongoDB to your PATH env if the option presents itself.
Once MongoDB is installed, there is a start script inside the database folder of the datachallenge project ```datachallenge/database/startmongo.bat``` which looks like this:
```
"C:\Program Files\MongoDB\Server\3.6\bin\mongod.exe" --dbpath .
```

After you have a running mongodb server (by running the startmongo.bat in command prompt, or running the former code above in terminal), make sure the config.py file inside the project directory is adjusted to your settings, which in most cases can be left default.

# Project libraries

The project is written in Python and thus requires python itself to run https://www.python.org/downloads/release/python-365/. 
For convenience, everything that needs to be included is already added to the project and therefore adding dependencies is not recommended and thus this section can be skipped. 
However, if you wish to download everything yourself, download and install python with the given link above.
Install all needed libraries which are listed below.
  
```
anytree	            2.4.3	
certifi	            2018.4.16	
chardet	            3.0.4	
cycler	            0.10.0	
idna	            2.7	
kiwisolver	    1.0.1	
matplotlib	    2.2.2	
nltk	            3.3	
numpy	            1.14.5	
oauthlib	    2.1.0	
pandas	            0.23.1	
pip	            9.0.3	
pymongo	            3.6.1	
pyparsing	    2.2.0	
python-dateutil	    2.7.3	
pytz	            2018.4	
requests	    2.19.1	
requests-oauthlib   1.0.0	
scipy	            1.1.0	
seaborn	            0.8.1	
setuptools	    39.0.1	
six	            1.11.0	
textblob	    0.15.1 
twython	            3.7.0 
urllib3	            1.23 
```

All of them can be installed using the following command.
```
pip install anytree certifi chardet cycler idna kiwisolver matplotlib nltk numpy oauthlib pandas pymongo pyparsing python-dateutil pytz requests requests-oauthlib scipy seaborn setuptools six textblob twython urllib3	            
```


# Running the project

Running the main.py script will return mostly every graph for the final poster. However, note that running the exact same script multiple times is not recommended.
For instance, creating the database should be done once so the following lines can be commented out (line 196 and 197) after running main.py once first:

```python
create_database()  # run this only once!
create_conversation_database()  # run this once too.
```

Starting from line 200, there are a few lines commented out. Uncomment the function to execute a given function which will either save a file inside the project folder (a graph) or will print information about the dataset. This depends on what exactly you want to generate, however only the bottom parts of ```main.py``` and ```data.py``` are relevant and all other scripts don't need any changes.


There is another file that returns graphs (stacked horizontal barcharts and the conversation throughout the year chart) which is the data.py file. This file contains hardcoded values which are printed by the ```find_sentiment_for_ids``` function on line 205 inside the main.py file. The datasets on top are basically pasted from the debug window and are used to create the graphs. This data obviously needs to be updated when the dataset changes which is a small limitation on our end.
Update the ```dataset``` variable on line 17 inside file data.py with the printed values inside the command prompt.


If you have everything pre-installed (first option inside the project libraries section), running the main.py works by opening command prompt and changing the current directory to the project location ```cd <PROJECT_LOCATION>``` first and then execute:

```
venv\Scripts\python.exe main.py
```

Or for data.py:

```
venv\Scripts\python.exe data.py
```
on the same command line interface.

This will either print requested information in the console or create a new graph (file inside current project). 

For option 2 (installing all dependencies manually), just run ```python.exe main.py``` or ```python.exe data.py``` since the libraries should be set up and resolved if ran properly.

 


Same applies for the graph that displays the conversation throughout the year run or ```sorted_over_year(22536055)``` on main.py and copy the values to ```year_data``` on line 379.

For more information about the changelog visit the github page at:
https://github.com/mertjuh/datachallenge/tree/dropped_conda