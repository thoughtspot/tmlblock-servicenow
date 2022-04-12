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


os.chdir('..')
file_path=Path( os.getcwd())
scripts=file_path/"SpotApps_Scripts/"
user_tml_path=file_path/"Input_Table_TML/"
source_path=file_path/"Spotapps_Original_TML/"
out_path=file_path/"Output_Spotapps/"
conn_path=file_path/"Input_Connection_YAML/"
csv_file=file_path/"Spotapps_Mapping.csv"
tml_file="Spotapps ServiceNow Incid.pinboard.tml"
out_file=out_path/tml_file
json_file=out_path/"Spotapps ServiceNow Incid_up.pinboard.json"

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def copy_tml():
    for filename in glob.glob(os.path.join(source_path, tml_file)):
        shutil.copy(filename, out_path)
copy_tml()

def csv_cols():
    file_1 = pd.read_csv(csv_file)
    file_2 = file_1[(file_1['Mapping Table'] == 'X')]
    file_3="'"+file_2['Worksheet Column Name'].str.replace(" ","")+"'"
    df=file_3.to_frame()
    return df;

def visualization_list():
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
    with open(out_path/"Spotapps ServiceNow Incid.pinboard_v1.json", 'w') as outfile:
        json.dump(os_list, outfile, indent=4)
        i_list = os_list['pinboard']['visualizations']
        viz_list = []
        for s_list in i_list:
            id_list = s_list['id']
            a_list = s_list['answer']['answer_columns']
            a=str(id_list)+":"+str(a_list).replace(' ','')
            viz_list.append(a)
        viz_df = pd.DataFrame(viz_list, columns=["Viz List"])
    return(viz_df);

def find_linenum(df , text):
    line_num = 0
    list=[]
    search_phrase = text
    for index, row in df.iterrows():
        line=str(row['Viz List'])
        line_num += 1
        if line.find(search_phrase) >= 0:
            print(line_num-1, file=open(out_path/"final_temp.txt", "a"))

def final_list(df1, df2):
    for index, row in df1.iterrows():
        line = row['Worksheet Column Name']
        find_linenum(df2,line)

def removed_list():
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        i_list = os_list['pinboard']['visualizations']
    def vis_removal_list():
        try:
            with open(out_path/"final_temp.txt") as f:
                lines = [int(line.rstrip()) for line in f]
                return (lines);
        except(FileNotFoundError):
            print('No visulization to be removed in the pinboard. Proceeding with the package creation.')
            os.remove(out_path/"Spotapps ServiceNow Incid.pinboard_v1.json")
            exit()
    i=vis_removal_list()
    new_list=()
    for ele in sorted(i, reverse = True):
        del i_list[ele]
    return(i_list);

def removed_layout_list():
    os_list1 = {}
    with open(out_file) as infile:
        os_list1 = yaml.load(infile, Loader=yaml.FullLoader)
        i_list = os_list1['pinboard']['layout']['tiles']
    def vis_removal_list1():
        with open(out_path/"final_temp.txt") as f:
            lines = [int(line.rstrip()) for line in f]
            return (lines);
    i=vis_removal_list1()
    for ele in sorted(i, reverse = True):
        del i_list[ele]
    return(i_list);

def pinboard_creation():
    i_list=removed_list()
    l_list=removed_layout_list()
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        guid = os_list['guid']
        p_name = os_list['pinboard']['name']
        i_json = json.dumps(i_list)
        jsonStr = json.dumps(l_list)
        print('{', file=open(json_file, "a"))
        print('    "guid": '+'"'+guid+'",', file=open(json_file, "a"))
        print('    "pinboard": {', file=open(json_file, "a"))
        print('        "name": "'+p_name+'",', file=open(json_file, "a"))
        print('        "visualizations": ', file=open(json_file, "a"))
        print(i_json+',', file=open(json_file, "a"))
        print('        "layout": {', file=open(json_file, "a"))
        print('          "tiles": ', file=open(json_file, "a"))
        print(jsonStr, file=open(json_file, "a"))
        print('        }', file=open(json_file, "a"))
        print('    }', file=open(json_file, "a"))
        print('}', file=open(json_file, "a"))

def pin_success():
    f = open(json_file,'r')
    print(yaml.dump(json.load(f),sort_keys=False),file=open(out_file, "w"))
    print("\n\nPinboard has been generated successfully in the user folder.")

def cleanup():
    os.remove(json_file)
    os.remove(out_path/"Spotapps ServiceNow Incid.pinboard_v1.json")
    os.remove(out_path/"final_temp.txt")

def pinboard_main():
    df1=csv_cols()
    if not df1.empty:
        df2=visualization_list()
        final_list(df1,df2)
        pinboard_creation()
        pin_success()
        cleanup()
    else:
        print('No visulization to be removed in the pinboard. Proceeding with the package creation.')
pinboard_main()
