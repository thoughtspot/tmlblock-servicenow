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

############To update the CSV mapping sheet#############

###############coverting the yaml to json###############
yaml_file=conn_path/'connection.yaml'
json_file=conn_path/'connection.json'
def yml_to_json():
    os_list = {}
    with open(yaml_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
    with open(json_file, 'w') as outfile:
        json.dump(os_list, outfile, indent=4)
    with open(json_file) as access_json:
        read_content = json.load(access_json)
        table_details = read_content['table']
        data=[]
        for table_dict in table_details:
            table_nm = table_dict['name'].replace(' ', '')
            column_details = table_dict['column']
            for col_list in column_details:
                col_nm = col_list['name'].lower().replace(' ', '')
                data.append([table_nm, col_nm])
        df = pd.DataFrame(data, columns=["Tables", "Columns"])
        os.remove(json_file)
        return df

########updating the CSV file######
def csv_update():
    df_temp=yml_to_json()
    file1=pd.read_csv(csv_file)
    file1['User Table Name'] = file1['User Table Name'].str.lower()
    file1['User Column Name'] = file1['User Column Name'].str.lower()
    Sub_Cols=pd.unique(df_temp['Tables'])
    Final_Tbl=pd.DataFrame(Sub_Cols,columns=['Tables'])
    df6=pd.merge(file1,Final_Tbl,left_on=['User Table Name'],right_on=['Tables'],how='left')
    df6['Missing Table'] = ['' if pd.isna(x)==False else 'Y' for x in df6['Tables']]
    df7=pd.merge(file1,df_temp,left_on=['User Table Name','User Column Name'],right_on=['Tables','Columns'],how='left')
    df7['Missing Column'] = ['' if pd.isna(x)==False else 'Y' for x in df7['Columns']]
    file1['Missing Table']=df6['Missing Table']
    file1['Missing Column']=df7['Missing Column']
    file1.loc[file1['Missing Table'] == 'Y', ['Missing Column']] = 'Y'
    file1.to_csv(csv_file,index=False)

def main():
    csv_update()
    output = 'Script completed'
    return output;
main()

####updating the reference table and column fields####
print ('Initial file update is complete. Proceeding with the mapping checker.')
print ('Checking completed.')

#######file checker and request the user to provide the input starts from here#######

#######To update the user input columns into our actual columns for rescanning purpose########
def merger():
    file_m = pd.read_csv(csv_file)
    file_m.loc[((file_m['Missing Table'] == 'Y') & (file_m['Mapping Table'].notnull()) | (file_m['Mapping Column'].notnull())), ['User Table Name']] = file_m['Mapping Table']
    file_m.loc[((file_m['Missing Column'] == 'Y') & (file_m['Mapping Table'].notnull()) | (file_m['Mapping Column'].notnull())), ['User Column Name']] = file_m['Mapping Column']
    file_m.to_csv(csv_file,index=False)
    merge_status='Columns updated'
    return(merge_status);

def tbl_col_checker():
        file1 = pd.read_csv(csv_file)
        file1.loc[((file1['Required Table'] == 'Y') & (file1['Missing Table'] == 'Y')) | (((file1['Required Column'] == 'Y')) & (file1['Missing Column'] == 'Y')), 'Check'] = 'Y'
        idx_num = file1.Check.eq('Y')
        if str(idx_num.any()) == "True":
                mapper='Still Unmapped'
        else:
                mapper='Mapped'
        return(mapper);

def revert():
    file_r = pd.read_csv(csv_file)
    file_r['User Table Name'] = file_r['Original Table Name']
    file_r['User Column Name'] = file_r['Original Column Name']
    file_r['Missing Column'] = ''
    file_r['Missing Table'] = ''
    #file_r['Referenced_Column'] = ''
    #file_r['Referenced_Table'] = ''
    file_r.to_csv(csv_file, index=False)
    revert_status='Mapping sheet changes reverted'
    return(revert_status);

def miss_col_display():
    data = pd.read_csv(csv_file,usecols=["User Table Name","User Column Name","Required Table","Missing Table","Missing Column"])
    df1=data[((data['Missing Table'] == 'Y')|(data['Missing Column'] == 'Y')) & (data['Required Table'] == 'Y')]
    df2=df1[["User Table Name","User Column Name","Missing Table","Missing Column"]]
    print(df2)

def rescan():
        mapper=tbl_col_checker()
        if mapper == "Still Unmapped":
                miss_col_display()
                print('Some of the mandatory column mappings are not avilable. Press "Y" to continue or "N" to exit:')
                Y_N = input()
                if str(Y_N).upper() == "Y":
                        print('Please update column N and Column O in the mapping doc for the missing table and column.Please enter "Y" once after the update is done to rescan the mapping document:')
                        ip2 = input()
                        if str(ip2).upper() == "Y":
                                merger()
                                main()
                                rescan()
                                print("All the required cols and tables are updated.")
                                r_status="Updated"
                        else:
                                print("Invalid command entered. Exiting the script.")
                                r_status = "Invalid"
                                exit()

                elif str(Y_N).upper() == "N":
                        print('If the required tables and columns are unmapped then we cannot proceed with the TML creations for the pinboards and worksheets.')
                        print('Please update column N and Column O in the mapping doc for the missing table and columns and then restart the process.')
                        revert()
                        r_status = "Invalid"
                        exit()
                else:
                        print("Invalid command entered")
                        revert()
                        r_status = "Invalid"
                        exit()
        else:
                r_status = "Updated"
        return(r_status);

def miss_col_display_non_req():
    data = pd.read_csv(csv_file,usecols=["User Table Name","User Column Name","Missing Table","Missing Column","Original Join Table Name","Join Required"])
    df1=data[(data['Missing Table'] == 'Y')|(data['Missing Column'] == 'Y') | (data['Original Join Table Name'].notnull() & data['Join Required'].isnull())]
    df2 = df1[["User Table Name", "User Column Name"]]
    print(df2)

def map_na():
    r_status=rescan()
    if r_status=="Updated":
        miss_col_display_non_req()
        file1 = pd.read_csv(csv_file)
        file1.loc[((file1['Missing Table'] == 'Y') | (file1['Missing Column'] == 'Y') | (file1['Original Join Table Name'].notnull() & file1['Join Required'].isnull())), 'Check'] = 'Y'
        idx_num = file1.Check.eq('Y')
        if str(idx_num.any()) == "True":
            print('There are few non required columns which are unmapped/not found. if you wish to remove them then please update the column N, O with "X". To proceed please enter "Y" or "N to disconnect:" ')
            print('Note: If you update these columns and tables as "X" then the answers/pinboards specific to these tables will be removed in the final output.')
            Y_N = input()
            if str(Y_N).upper() == "Y":
                file_r = pd.read_csv(csv_file)
                file_r.loc[file_r['Mapping Table'] == 'X', ['User Table Name']] = ''
                file_r.loc[file_r['Mapping Column'] == 'X', ['User Column Name']] = ''
                file_r.to_csv(csv_file, index=False)
                print("\n\n\bMapping document has been updated. Proceeding with the table TML updations.\b\n\n")
                na_status = 'Columns updated'
            elif str(Y_N).upper() == "N":
                print('Disconnecting')
                revert()
                exit()
            else:
                print('Invalid Command')
                revert()
                exit()
        else:
            na_status = 'Columns updated'
    else:
        na_status = 'Columns not updated'
        print('Mapping sheet not updated properly. Exiting the script')
        exit()
    return(na_status);
map_na()
