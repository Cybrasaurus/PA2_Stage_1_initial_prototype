"""
        author: Adrian Scheubrein
        date: 25.01.2022
        version: 1.2.1
        license: MIT
"""
import pandas as pd
import config_handling as my_ch
import data_get_raw as my_dgr
import json


def rawdatacleaner(excel_to_load,cwd_path):

    try:
        #get a dictionary of the the excel file names containing the raw data
        excel_name_dict=my_ch.read_config(cwd_path=cwd_path)[0]
        #get the file name of the excel containing the raw data
        excel_file_name=excel_name_dict[excel_to_load]
        #load the contents of the excel as a pandas dataframe and return it
        loaded_df = pd.read_excel(f"{cwd_path}/Raw_Excels/{excel_file_name}.xlsx")
    

        cleaning_df= loaded_df
        #drop all rows and columns with only Nan Values
        cleaning_df=cleaning_df.dropna(how="all")

        column_names=list(cleaning_df.columns)
        
        #get list of all column Names
        outlist=[]
        for items in column_names:
            if items[:8]!="Unnamed:":
                outlist.append(items)
        

        #raw data excel "starts" in column R, previous ones are hidded and irrelevant for code
        #first relevant column has the header "Länderbasierter... | Date". Since the date changes with each new export, grab exact name here
        for items in outlist:
            if items[:36]=="Länderbasierter Projektplan KEY_2_LONG":
                my_colname=items

        #get location of first relevant column as integer
        my_colindex=cleaning_df.columns.get_loc(my_colname)
        #drop first 4 rows and all columns left of first relevant one
        cleaning_df=cleaning_df.iloc[5:,my_colindex:] 
        #list to rename column headers
        my_header_list=["Activity Number", "Activity Subject", "Country", "Phase",
        "SENSITIVE DATA CENSORING 1", "SENSITIVE DATA CENSORING 2","SENSITIVE DATA CENSORING 3", "SENSITIVE DATA CENSORING 4","remove 1", "remove 2", "Start Date",
        "End Date"]
        #get list of current column headers
        reduced_col_name_list=list(cleaning_df.columns)
        #rename part of list
        reduced_col_name_list[0:12]=my_header_list
        #rename column headers
        cleaning_df.columns=reduced_col_name_list

        #drop columns to the right of "End Date", contain a gannt chart
        my_colindex_enddate=cleaning_df.columns.get_loc("End Date")
        cleaning_df=cleaning_df.iloc[:,:my_colindex_enddate+1]

        #drop unneeded columns
        cleaning_df=cleaning_df.drop(columns={"Dependencies", "SENSITIVE DATA CENSORING","remove 1", "remove 2"})

        #clean up remaining code
        cleaning_df=cleaning_df.iloc[4:,:]
        cleaning_df=cleaning_df.dropna(how="all")
        cleaning_df=cleaning_df.replace("-", "")
        cleaning_df=cleaning_df.replace("Gesamt", "ALL")


        #dict to translate KEY_2_LONG "Verantwortlicher Fachbereich" to "SIT BC"
        my_dataDictList = cleaning_df.to_dict("records")
        KEY_2_SHORT_TranslationDict = {
            "SENSITIVE DATA CENSORING":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 1":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 2":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 3":"",
            "SENSITIVE DATA CENSORING 4":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 5":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 6":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 7":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 8":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 9":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 10":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 11":"SENSITIVE DATA CENSORING",
            "SENSITIVE DATA CENSORING 12":"SENSITIVE DATA CENSORING",
        }
        #rename KEY_2_LONG "Verantwortlicher Fachbereich" to "SIT BC"
        for items in range(len(my_dataDictList)):
            try:
                my_dataDictList[items]["SENSITIVE DATA CENSORING"]=KEY_2_SHORT_TranslationDict[my_dataDictList[items]["SENSITIVE DATA CENSORING"]]
            except:
                pass
        
        #add Solution to Projects from the raw_excel_projecteUndID
        projectAndID_df=my_dgr.get_project_and_id()
        for items in range(len(my_dataDictList)):
            my_dataDictList[items]["Affected Solution"]=""
            for project_numbers in projectAndID_df:
                #print(my_dataDictList[items])
                
                if my_dataDictList[items]["Activity Number"]==(project_numbers["Project number"]):
                    my_dataDictList[items]["Affected Solution"]=project_numbers["Solution"]
                    #print(my_dataDictList[items]["Activity Number"], " / ", project_numbers["Project number"], "-> ",project_numbers["Solution"])
                    #print(my_dataDictList[items])
        return my_dataDictList
                    
                        
                
                    


    except KeyError:
        print("get_raw_data load_excel -- Invalid Key for Dictionary")
    except FileNotFoundError:
        print("get_raw_data load_excel -- Could not find File or Directory. Please double check if the raw excels are in the correct folder and the config has the right names")

