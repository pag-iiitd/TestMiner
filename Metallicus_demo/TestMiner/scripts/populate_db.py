"""
This file contains the code to populate database from excel file.

A few manual queries are required before we start to use the database.

UPDATE Functions SET documentation=NULL where documentation='nan';
VACUUM;
"""


import pandas as pd
import numpy as np
from init_db import Functions, Cluster_Functions


def getFnName(code):

    name = None
    defLoc = str(code).find("def ")
    bracketLoc = str(code).find("{")

    if defLoc == -1 and bracketLoc == -1:
        #in this case, the code must one of the name(); cases...?
        temp1 = str(code).split(";", 1)[0]
        parLoc = temp1.rfind("(")
        if parLoc != -1:
            temp2 = temp1[:parLoc]
            spaceLoc = temp2.rfind(" ")

            if(spaceLoc) != -1:
                temp3 = temp2[spaceLoc:]
                name = temp3
            else:
                #pass
                name = None
        else:
            #pass
            name = None

    elif bracketLoc == -1:
        #only def exists
        temp1 = code.split("def ", 1)[1]
        temp2 = temp1.split("(", 1)[0]
        if "u'" in temp2:
            temp3 = temp2.split("u'")[1]
        else:
            temp3 = temp2
        name = temp3

    elif defLoc == -1:
        #no def exists, only {. pure java case
        temp1 = code.split("{", 1)[0]
        lastParIndex = temp1.rfind("(")
        temp2 = temp1[:lastParIndex]
        lastSpIndex = temp2.rfind(" ")
        temp3 = temp2[lastSpIndex:lastParIndex]
        name = temp3

    elif defLoc < bracketLoc:
        #word def is before first bracket. python case
        temp1 = code.split("def ", 1)[1]
        temp2 = temp1.split("(", 1)[0]
        if "u'" in temp2:
            temp3 = temp2.split("u'")[1]
        else:
            temp3 = temp2
        name = temp3

    elif bracketLoc < defLoc:
        #bracket { is before occurence of word def. java case
        temp1 = code.split("{", 1)[0]
        lastParIndex = temp1.rfind("(")
        temp2 = temp1[:lastParIndex]
        lastSpIndex = temp2.rfind(" ")
        temp3 = temp2[lastSpIndex:lastParIndex]
        name = temp3

    else:
        name = None

    return name


def convert_test_path_file_to_dict(excel_file_path, sheet_name):
    res_dict = {}
    excel_file = pd.ExcelFile(excel_file_path)
    dataframe = excel_file.parse(sheet_name)
    print(len(dataframe['src_path']))
    for index, row in dataframe.iterrows():
        res_dict[row['src_path']] = row['test_path']
    return res_dict


def populate_db(excel_file_path, sheet_name, test_fp_dict):
    """Generate SqlLite Dataset from the excel file."""
    excel_file = pd.ExcelFile(excel_file_path)
    dataframe = excel_file.parse(sheet_name)

    for index, row in dataframe.iterrows():
        try:
            Functions.create(fn_id=row['ID'],
                             fn_signature=row['function_sig'],
                             documentation=row['docstring'],
                             repo_path=row['repo_path'],
                             library_name=row['repo_name'],
                             code=row['method'],
                             test_fp=test_fp_dict.get(row['repo_path']))
            if index % 1000 == 0:
                print('Batch Finished with index :{}'.format(index))
        except Exception as e:
            print(e)
            print('Index: {}'.format(index))
            print(row['method'])
            print(row['repo_path'])
            print(row['repo_name'])
            print(row['docstring'])


def populate_cluster_mapping(excel_file_path, sheet_name):
    """."""
    excel_file = pd.ExcelFile(excel_file_path)
    dataframe = excel_file.parse(sheet_name)
    for index, row in dataframe.iterrows():
        try:
            Cluster_Functions.create(fn_id=row['ID'], cluster_id=row['CID'])
            if index % 10000 == 0:
                print('Batch Finished with index :{}'.format(index))
        except Exception as e:
            print(e)
            print('Index: {}'.format(index))


if __name__ == "__main__":
    test_fp_dict = convert_test_path_file_to_dict('/home/monk/Repos/matched_test_paths_combined.xlsx', 'Sheet1')
    # print(len(test_fp_dict))
    populate_db('/home/monk/Repos/Functions_data2_combined.xlsx', 'Sheet1', test_fp_dict)
    populate_cluster_mapping('/home/monk/Repos/CrossLibTest/dataset/cluster_data_combined.xlsx', 'Sheet1')
