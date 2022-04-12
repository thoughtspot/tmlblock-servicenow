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
tml_file="Spotapps_Servicenow_Incid.worksheet.tml"
out_file=out_path/tml_file
line_file=out_path/"line_num.txt"

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def copy_tml():
    for filename in glob.glob(os.path.join(source_path, tml_file)):
        shutil.copy(filename, out_path)
copy_tml()

def rename_table():
    col_list = ["Original Table Name", "User Table Name"]
    file_r = pd.read_csv(csv_file, usecols=col_list)
    dups = file_r.drop_duplicates().dropna()
    dups['match'] = dups.apply(lambda x: 'Y' if x['Original Table Name'] == x['User Table Name'] else 'N', axis=1)
    final_recs = dups[(dups.match == 'N')]
    for index, row in final_recs.iterrows():
        new_table = row['User Table Name']
        old_table = row['Original Table Name']
        with fileinput.FileInput(out_file, inplace=True, backup='.bak') as file:
            for line in file:
                ip_old = r"\b" + old_table + r"\b"
                print(re.sub(ip_old, new_table, line), end='')
rename_table()

def rename_table_1():
    col_list = ["Original Table Name", "User Table Name"]
    file_r = pd.read_csv(csv_file, usecols=col_list)
    dups = file_r.drop_duplicates().dropna()
    dups['match'] = dups.apply(lambda x: 'Y' if x['Original Table Name'] == x['User Table Name'] else 'N', axis=1)
    final_recs = dups[(dups.match == 'N')]
    for index, row in final_recs.iterrows():
        new_table = row['User Table Name']
        old_table = row['Original Table Name']
        with fileinput.FileInput(out_file, inplace=True, backup='.bak') as file:
            for line in file:
                ip_old = ' ' + old_table + '_to_'
                new = ' ' + new_table + '_to_'
                print(re.sub(ip_old, new, line), end='')
rename_table_1()

def rename_table_2():
    col_list = ["Original Table Name", "User Table Name"]
    file_r = pd.read_csv(csv_file, usecols=col_list)
    dups = file_r.drop_duplicates().dropna()
    dups['match'] = dups.apply(lambda x: 'Y' if x['Original Table Name'] == x['User Table Name'] else 'N', axis=1)
    final_recs = dups[(dups.match == 'N')]
    for index, row in final_recs.iterrows():
        old_table = row['Original Table Name']
        new_table = row['User Table Name']
        with fileinput.FileInput(out_file, inplace=True, backup='.bak') as file:
            for line in file:
                ip_1 = '_to_' + old_table + '\n'
                new_1 = '_to_' + new_table + '\n'
                print(re.sub(ip_1, new_1, line), end='')
rename_table_2()

def rename_table_3():
    col_list = ["Original Table Name", "User Table Name"]
    file_r = pd.read_csv(csv_file, usecols=col_list)
    dups = file_r.drop_duplicates().dropna()
    dups['match'] = dups.apply(lambda x: 'Y' if x['Original Table Name'] == x['User Table Name'] else 'N', axis=1)
    final_recs = dups[(dups.match == 'N')]
    for index, row in final_recs.iterrows():
        old_table = row['Original Table Name']
        new_table = row['User Table Name']
        with fileinput.FileInput(out_file, inplace=True, backup='.bak') as file:
            for line in file:
                ip_1 = '_to_' + old_table + ''
                new_1 = '_to_' + new_table + ''
                print(re.sub(ip_1, new_1, line), end='')
rename_table_3()

def rename_coulmn():
    col_list = ["User Table Name", "User Column Name", "Original Table Name", "Original Column Name"]
    file_r = pd.read_csv(csv_file, usecols=col_list)
    dups = file_r.drop_duplicates().dropna()
    dups['match'] = dups.apply(lambda x: 'Y' if x['User Table Name'] == x['Original Table Name'] and x['User Column Name'] == x['Original Column Name'] else 'N', axis=1)
    final_recs = dups[(dups.match == 'N')]
    for index, row in final_recs.iterrows():
        a = row['Original Table Name'] + '_1::' + row['Original Column Name']
        b = row['Original Table Name'] + '_1::' + row['User Column Name']
        with fileinput.FileInput(out_file, inplace=True, backup='.bak') as file:
            for line in file:
                a_old = r"\b" + a + r"\b"
                print(re.sub(a_old, b, line), end='')
rename_coulmn()

def read_tbl_wn_nm():
    col_list=["Original Table Name","User Table Name","Mapping Table","Worksheet Column Name"]
    file_r = pd.read_csv(csv_file, usecols=col_list)
    df1 = file_r[(file_r['Mapping Table'] == 'X')]
    df1['User Table Name'].fillna(df1['Original Table Name'], inplace=True)
    a=df1['User Table Name'].drop_duplicates().rename('T/C Name')
    b=df1['Worksheet Column Name'].drop_duplicates().rename('T/C Name')
    return a,b;
read_tbl_wn_nm()

def worksheet_list():
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        a_list = os_list['worksheet']['tables']
        tbl_df = pd.DataFrame({'Names':a_list})
        j_list = (os_list['worksheet']['joins'])
        jn_list = []
        for temp_list in j_list:
            des_list = temp_list['destination']
            jn_list.append([des_list])
        jn_df = pd.DataFrame(jn_list, columns=["Names"])
        cols_list = os_list['worksheet']['worksheet_columns']
        wc_list = []
        for s_list in cols_list:
            col_name = s_list['name']
            wc_list.append([col_name])
        wc_df = pd.DataFrame(wc_list, columns=["Names"])
        tbl_list = os_list['worksheet']['table_paths']
        tbp_list = []
        for k_list in tbl_list:
            tbl_name = k_list['table']
            tbp_list.append([tbl_name])
        tbp_df = pd.DataFrame(tbp_list, columns=["Names"])
    return tbl_df,jn_df,wc_df,tbp_df;
worksheet_list()

def find_linenum(df , text):
    line_num = 0
    list=[]
    search_phrase = text
    for index, row in df.iterrows():
        line=str(row['Names'])
        line_num += 1
        if line.find(search_phrase) >= 0:
            print(line_num-1, file=open(line_file, "a"))

def final_list(df1, df2):
    a=df1.to_frame()
    for index, row in a.iterrows():
        line = row['T/C Name']
        find_linenum(df2,line)

def remove_table_list():
    table_list_df, wn_list_df = read_tbl_wn_nm()
    tbl_df, jn_df, wc_df, tbp_df = worksheet_list()
    final_list(table_list_df, tbl_df)
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        a_list = os_list['worksheet']['tables']
    def tbl_removal_list():
        with open(line_file) as f:
            lines = [int(line.rstrip()) for line in f]
            return (lines);
    k=tbl_removal_list()
    i=[]
    for o in k:
        if o not in i:
            i.append(o)
    for ele in sorted(i, reverse = True):
        del a_list[ele]
    os.remove(line_file)
    return(a_list)

def remove_join_list():
    table_list_df, wn_list_df = read_tbl_wn_nm()
    tbl_df, jn_df, wc_df, tbp_df = worksheet_list()
    final_list(table_list_df, jn_df)
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        j_list = (os_list['worksheet']['joins'])
        def join_removal_list():
            with open(line_file) as f:
                lines = [int(line.rstrip()) for line in f]
            return (lines);
        k=join_removal_list()
        i = []
        for o in k:
            if o not in i:
                i.append(o)
        for ele in sorted(i, reverse = True):
            del j_list[ele]
        os.remove(line_file)
        return(j_list)

def remove_tbp_list():
    table_list_df, wn_list_df = read_tbl_wn_nm()
    tbl_df, jn_df, wc_df, tbp_df = worksheet_list()
    final_list(table_list_df, tbp_df)
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        tbp_list = os_list['worksheet']['table_paths']
        def tbp_removal_list():
            with open(line_file) as f:
                lines = [int(line.rstrip()) for line in f]
            return (lines);
        k = tbp_removal_list()
        i = []
        for o in k:
            if o not in i:
                i.append(o)
        for ele in sorted(i, reverse=True):
            del tbp_list[ele]
        os.remove(line_file)
        return (tbp_list)

def remove_wn_list():
    table_list_df, wn_list_df = read_tbl_wn_nm()
    tbl_df, jn_df, wc_df, tbp_df = worksheet_list()
    final_list(wn_list_df, wc_df)
    os_list = {}
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        cols_list = os_list['worksheet']['worksheet_columns']
        def wn_removal_list():
            with open(line_file) as f:
                lines = [int(line.rstrip()) for line in f]
            return (lines);
        k = wn_removal_list()
        i = []
        for o in k:
            if o not in i:
                i.append(o)
        for ele in sorted(i, reverse=True):
            del cols_list[ele]
        os.remove(line_file)
        return (cols_list)

def worksheet_generation():
    file_json=out_path/"Spotapps_Servicenow_Incid.worksheet.json"
    tbl_list=remove_table_list()
    jn_list=remove_join_list()
    tbp_l=remove_tbp_list()
    wn_l=remove_wn_list()
    with open(out_file) as infile:
        os_list = yaml.load(infile, Loader=yaml.FullLoader)
        guid = os_list['guid']
        w_name = os_list['worksheet']['name']
        properties=os_list['worksheet']['properties']
        tbl_json=json.dumps(tbl_list)
        jn_json=json.dumps(jn_list)
        tbp_json=json.dumps(tbp_l)
        wn_json=json.dumps(wn_l)
        prop_json=json.dumps(properties, indent = 4)
        print('{', file=open(file_json, "a"))
        print('    "guid": ' + '"' + guid + '",', file=open(file_json, "a"))
        print('    "worksheet": {', file=open(file_json, "a"))
        print('        "name": '+ '"' + w_name + '",', file=open(file_json, "a"))
        print('        "tables": ' + tbl_json + ',', file=open(file_json, "a"))
        print('        "joins": ' + jn_json + ',', file=open(file_json, "a"))
        print('        "table_paths": ' + tbp_json + ',', file=open(file_json, "a"))
        try:
            formula = os_list['worksheet']['formulas']
            formula_json = json.dumps(formula, indent=4)
            print('        "formulas": ' + formula_json + ',', file=open(file_json, "a"))
        except(KeyError):
            status = 'No Formulas'
        print('        "worksheet_columns": ' + wn_json + ',', file=open(file_json, "a"))
        print('        "properties": ' + prop_json, file=open(file_json, "a"))
        print('    }', file=open(file_json, "a"))
        print('}', file=open(file_json, "a"))

def os_cleanup():
    os.remove(out_path/"Spotapps_Servicenow_Incid.worksheet.json")
    os.remove(out_path/"Spotapps_Servicenow_Incid.worksheet.tml.bak")

def tml_success():
    f = open(out_path/"Spotapps_Servicenow_Incid.worksheet.json",'r')
    print(yaml.dump(json.load(f),sort_keys=False), file=open(out_file, "w"))
    print("\n\nWorksheet has been generated successfully in the user folder. Proceeding with the pinboard creation.")

def worksheet_main():
    table_list_tmp,wn_list_tmp =read_tbl_wn_nm()
    if not table_list_tmp.empty & wn_list_tmp.empty:
        worksheet_list()
        worksheet_generation()
        tml_success()
        os_cleanup()
    else:
        print('No columns to be deleted in the worksheet. Proceeding with the pinboard generation.')
        os.remove(out_path/'Spotapps_Servicenow_Incid.worksheet.tml.bak')
worksheet_main()