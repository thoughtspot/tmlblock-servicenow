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
#os.getcwd()
user_tml_path=file_path/"Input_Table_TML/"
source_path=file_path/"Spotapps_Original_TML/"
out_path=file_path/"Output_Spotapps/"
conn_path=file_path/"Input_Connection_YAML/"
csv_file=file_path/"Spotapps_Mapping.csv"

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def copy_tml():
    try:
        for filename in glob.glob(os.path.join(user_tml_path, '*.tml')):
            shutil.copy(filename, out_path)
    except:
        print("Please place the table tml files in the Input_Table_TML folder and rerun the script.")
        exit()
copy_tml()

def join_lis(user_name):
    col_list=["User Table Name", "User Column Name", "Original Join Table Name", "Original Join Column Name","Join type"]
    dataframe1 = pd.read_csv(csv_file, usecols=col_list)
    df1 = dataframe1[((dataframe1['Original Join Table Name'].notnull()) & (dataframe1['User Table Name'].notnull()))]
    df2 = df1[(df1['User Table Name'] == user_name)]
    if not df2.empty:
        df3=df2[df2.duplicated(subset=['User Table Name','Original Join Table Name'], keep=False)]
        df3['repeat_col']=df3['User Column Name']
        df4 = pd.merge(df2, df3, left_on=['User Table Name', 'User Column Name'], right_on=['User Table Name', 'User Column Name'], how='left')
        col_list_2=['Original Table Name','Original Column Name','User Table Name','User Column Name']
        df5=pd.read_csv(csv_file, usecols=col_list_2).drop_duplicates()
        df6=pd.merge(df4,df5,left_on=['Original Join Table Name_x','Original Join Column Name_x'], right_on=['Original Table Name','Original Column Name'], how='left')
        df7=df6[['User Table Name_x','User Column Name_x','User Table Name_y','User Column Name_y','Join type_x','repeat_col']]
        df=df7[(df7['User Table Name_y'].notnull()) | (df7['User Column Name_y'].notnull())]
    else:
        df = pd.DataFrame()
    return df;

def append_tml(user_name,user_tml):
    df1= join_lis(user_name)
    if not df1.empty:
        lines = "  joins_with:\n"
        with open(user_tml, 'a') as f:
            f.writelines(lines)
        for index, row in df1.iterrows():
            s_t = row['User Table Name_x']
            s_c = row['User Column Name_x']
            t_t = row['User Table Name_y']
            t_c = row['User Column Name_y']
            r_c = row['repeat_col']
            join_type = row['Join type_x']
            if str(r_c).replace('nan', 'X') == 'X':
                print('  - name: ' + s_t + '_to_' + t_t, file=open(user_tml, "a"))
            else:
                print('  - name: ' + s_t + '_to_' + t_t + '_' + str(r_c), file=open(user_tml, "a"))
            print('    destination:', file=open(user_tml, "a"))
            print('      name: '+t_t, file=open(user_tml, "a"))
            print('    "on": "(['+s_t+'::'+s_c+'] = ['+t_t+'::'+t_c+'])"', file=open(user_tml, "a"))
            print('    type: '+join_type, file=open(user_tml, "a"))
            print('    is_one_to_one: true', file=open(user_tml, "a"))
    else:
        print("No Joins to be updated in "+user_tml)

def update_alltmls():
    file1 = pd.read_csv(csv_file)
    file1.loc[((file1['Original Join Table Name'].notnull()) & (file1['User Table Name'].notnull())), 'Check'] = 'Y'
    idx_num = file1.Check.eq('Y')
    if str(idx_num.any()) == "True":
        print('Enter "Y" to proceed with the updation of the TML with join conditions, else "N" to Exit:')
        print('Note: If you have updated the mappings as "X" then the joins to those tables will be removed in the final output.')
        Y_N = input()
        if str(Y_N).upper() == "Y":
            col_list = ["User Table Name", "Mapping Table"]
            df1 = pd.read_csv(csv_file, usecols=col_list, index_col=False)
            df2 = df1[(df1['Mapping Table'] != 'X')].drop_duplicates()
            df2["user_tml"] =  str(out_path)+'/' + df2["User Table Name"] + '.table.tml'
            df3 = df2[["User Table Name", "user_tml"]]
            for index, row in df3.iterrows():
                u_n = row['User Table Name']
                u_t = row['user_tml']
                print("Updation of the table " + u_t + " has been started.")
                append_tml(u_n,u_t)
                print("Updation of the table " + u_t + " has been completed.")
        elif str(Y_N).upper() == "N":
            exit()
        else:
            print('Invalid command entered. Exiting the script')
            exit()
    print("\n\nAll the user table TML's have been updated with the required joins successfully. Proceeding with worksheet tml generation.")
update_alltmls()