# Group 1 datachallenge assignment

This repository contains the source code for the final poster. All the information that is displayed on the poster is gathered using the algorithms inside this project.

To run this project, make sure an instance of mongodb is running. By default, there is a start script inside the database folder which looks like this:
```
"C:\Program Files\MongoDB\Server\3.6\bin\mongod.exe" --dbpath .
```

After you have a running mongodb server, make sure the config.py file is adjusted to your settings.

Running the main.py script will return mostly every graph for the final poster. However, note that running the exact same script multiple times is not recommended.
For instance, creating the database should be done once so the following lines can be commented out (line 196 and 197):

```python
create_database()  # run this only once!
create_conversation_database()  # run this once too.
```

Starting from line 200, there are a few lines commented out. Uncomment the function to execute a given function which will either save a file inside the project folder (a graph) or will print information about the dataset.


There is another file that returns graphs which is the data.py file. This file contains hardcoded values which are printed by the ```find_sentiment_for_ids``` function on line 205 or ```sorted_over_year(22536055)``` inside the main.py file. The datasets on top are basically pasted from the debug window and are used to create the graphs. This data obviously needs to be updated when the dataset changes which is a small limitation on our end.


For more information about the changelog visit the github page at:
https://github.com/mertjuh/datachallenge/tree/dropped_conda