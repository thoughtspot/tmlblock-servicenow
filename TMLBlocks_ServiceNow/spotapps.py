import csv
import re,os
import yaml
import json
import sys
import time
import fileinput
import pandas as pd
from csv import reader
import simplejson as json
from pathlib import Path
from zipfile import ZipFile
import shutil
import glob
import warnings
import pandas as pd
from pandas.core.common import SettingWithCopyWarning

file_path= Path(os.getcwd())
scripts=file_path/"SpotApps_Scripts/"
os.chdir(scripts)
user_tml_path=file_path/"Input_Table_TML/"
source_path=file_path/"Spotapps_Original_TML/"
out_path=file_path/"Output_Spotapps/"
conn_path=file_path/"Input_Connection_YAML/"

############Running script to update the CSV mapping sheet#############
try:
    exec(open('1_v1.py').read())
except:
    print("Issue occured during the CSV updation.")
    exit()

############Starting script to update the table TML's#############
os.chdir(scripts)
try:
    exec(open('2_v1.py').read())
except():
    print("Issue occured during the Table Tml updation.")
    exit()

############Starting script to update the worksheet#############
os.chdir(scripts)
try:
    exec(open('3_v1.py').read())
except():
    print("Issue occured during the Worksheet updation.")
    exit()

os.chdir(scripts)
try:
    exec(open('5_v1.py').read())
except():
    print("Issue occured during the Worksheet updation.")
    exit()

############SStarting script to update the Pinboard#############
os.chdir(scripts)
try:
    exec(open('4_v1.py').read())
except():
    print("Issue occured during the Pinboard updation.")
    exit()

#####################creating the package(ZIP) in user folder###########################
print("\n\nPackage creation has been started.")
def zip_package():
    os.chdir(out_path)
    file_list = os.listdir()
    for file in file_list:
        zipObj = ZipFile('Spotapps_servicenow.zip', 'a')
        zipObj.write(file)
        zipObj.close()
zip_package()

print('\n\nPackage has been created successfully inside the Output_Spotapps folder. Please import the same into Thoughtspot Champagne.')