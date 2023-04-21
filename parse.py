# sat3310
# Final Project
# created by Mia-Y-Kelly
# This script identifies all concerning entries in the mongod log file
# and writes them to a separate file. It has two modes: running once (1) or
# running constantly if the mongod process is active (2).

# Imports
import json
from pathlib import Path
from time import sleep
import os

# This function isolates all concerning mongod entries writes them to a file
# It returns the timestamp last_modified. last_modified is used to determine
# if the log file needs to be checked again when on the second mode.
def parse(debug):
    # Variables
    path = "/var/log/mongodb/mongod.log"
    last_modified = Path(path).stat().st_mtime    # Store the last time the file was modified
    entry_list = list()
    all_entries = dict()        # Used for debugging
    important = dict()
    entry = dict()

    # Read entire file to fin as a string
    fin = open(path,"r")
    entry_list = fin.readlines()
    fin.close()

    
    '''
    Severity Level | Description
    -----------------------------
    F                   Fatal
    E                   Error
    W                   Warning
    I                   Informational
    D1-D5               Debug

    We only care about the F,E,W logs
    '''
    for i in entry_list:
        # Only add if it contains more than whitespace
        if not i.isspace():
            entry = json.loads(i)
            datetime = entry.pop("t")['$date']  # Extract the datetime for the id
            
            # Used for debugging
            if debug:
                all_entries.update({datetime : entry})
            
            # Extract the severity
            severity = (all_entries.get(datetime)).get('s')

            # Add the entry if it is F/E/W
            if severity == 'F' or severity == 'E' or severity == 'W':
                important.update({datetime: entry})
                
    # Write all concerning entries to file
    fname = "logs_filtered"
    fout = open(fname + ".log", "w")           
    pretty_str = json.dumps(important, indent=4)
    fout.write(pretty_str)
    fout.close()

    # debug
    if debug:
        # Pretty print the file (make sure all the JSON is human-readable)
        pretty_str = json.dumps(all_entries, indent=4)
        fout = open("debug.log", "w")
        fout.write(pretty_str)
        fout.close()

    return last_modified


# Main
RUN_ONCE = None
debug = True

# Have user chose mode; sanitize input
while(RUN_ONCE != "1" or RUN_ONCE != "2"):
    RUN_ONCE = input("Run once (1) or constantly (2): ")   # Script can either run once or constantly
    if(RUN_ONCE == "1" or RUN_ONCE == "2"):
        break

# Run once no matter what
prev = parse(debug)

# Start the inifinite loop is the user wants to run the script in the background.
if RUN_ONCE == "2":
    if not debug:
        # set frequency the mongod.log is checked for new entries in seconds (every half hour)
        INTERVAL = 1800
    else:
        # set frequency shorter when testing
        INTERVAL = 5

    while(len(list(os.popen("ps -C mongod"))) == 2):
        if(prev != Path("/var/log/mongodb/mongod.log").stat().st_mtime):
            print("New entries discovered...checking mongod.log")
            prev = parse(debug)
        sleep(INTERVAL)
    print("mongod process is not running...stopping parse.py")




