"""
        author: Adrian Scheubrein
        date: 25.01.2022
        version: 1.2.1
        license: MIT
"""
import data_get_raw as my_dgr
import pandas as pd
import copy

def clean_raw_excel(excel_to_load:str, cwd_path:str):
    #read the excel file, gets returned as List of Dictionaries, convert it back to a pandas dataframe
    raw_datadict=my_dgr.load_excel(excel_to_load, cwd_path)
    raw_pandas_df=pd.DataFrame(data=raw_datadict, dtype=object)

    #fill nan values
    processing_df=raw_pandas_df.fillna("")
    #remove first 7 rows, last column
    processing_df=processing_df.iloc[7:,:-1]
    #drop unused columns
    processing_df=processing_df.drop(columns={"Unnamed: 5", "Unnamed: 6", "Unnamed: 7"})

    #grab values of the topmost row of the df, i.e. the countries in which the project gets rolled out to
    my_numpy_ndarray=processing_df.values[0]
    #convert type to a list
    project_country_list=my_numpy_ndarray.tolist()
    #add these to the list
    project_country_list[0:5]=["SENSITIVE DATA CENSORING","SENSITIVE DATA CENSORING","SENSITIVE DATA CENSORING Name", "SENSITIVE DATA CENSORING","SENSITIVE DATA CENSORING"]
    #rename all columns of the df
    processing_df.columns=project_country_list
    #drop first and last 2 rows
    processing_df=processing_df.iloc[1:-2,:]
    #only keep every other row. Raw data has combined cells, every other row is empty
    processing_df=processing_df.iloc[::2,]

    #rename X to COMPANY DATA CENSOR
    processing_df=processing_df.replace("X", "KEY_1_LONG COMPANY DATA CENSOR")

    #add the activity Number and Affected Solution columns, are empty, get filled below
    processing_df_lenght=len(processing_df.index)
    emptylist=[]
    for i in range(processing_df_lenght):
        emptylist.append("")
    processing_df.insert(0, "SENSITIVE DATA CENSORING SENSITIVE DATA CENSORING",emptylist, True)
    processing_df.insert(0, "SENSITIVE DATA CENSORING SENSITIVE DATA CENSORING",emptylist, True)




    #convert the cleaned df back to a list of dictionaries
    cleaned_datadict=processing_df.to_dict("records")
    
    #Dict to Translate KEY_1_LONG Ressort to KEY_3_LONG BC
    KEY_1_SHORT_TranslationDict = {
    "SENSITIVE DATA CENSORING":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 1":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 2":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 3":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 4":"",
    "SENSITIVE DATA CENSORING 5":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 6":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 7":"SENSITIVE DATA CENSORING",
    "KEY_1_LONG SENSITIVE DATA CENSORING":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 8":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 9":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 10":""
}
    #Rename Ressort to BC in DF
    for items in range(len(cleaned_datadict)):
        try:
            cleaned_datadict[items]["SENSITIVE DATA CENSORING"]=KEY_1_SHORT_TranslationDict[cleaned_datadict[items]["SENSITIVE DATA CENSORING"]]
        except:
            pass
    
    #fill column activity Number and Affected Solution with data from the Projects Excel
    projectAndID_df=my_dgr.get_project_and_id()
    for items in range(len(cleaned_datadict)):
        for project_numbers in projectAndID_df:
            if str.lower(cleaned_datadict[items]["SENSITIVE DATA CENSORING Name"])==str.lower(project_numbers["Project Name"]):
                cleaned_datadict[items]["Affected SENSITIVE DATA CENSORING"]=project_numbers["SENSITIVE DATA CENSORING"]
                cleaned_datadict[items][" SENSITIVE DATA CENSORING"]=project_numbers["SENSITIVE DATA CENSORING"]

    
    

    return cleaned_datadict

def dictsorter(input_datadict):
    """This function takes the first 7 columns of the df (the non-country columns) and adds them to the output
    Then a new dictionary is made for every country, effectively making a new row for every country

    Args:
        input_datadict ([List of Dictionaries]): [The List of dictionaries from clean_raw_excel()]

    Returns:
        [List of Dictionaries]: [a list of dictionaries, with a dictionary for every Project/Country Combo]
    """
    my_new_datadict = []
    
    for dicts in input_datadict:
        i=0
        outdict={}
        for keys in dicts:
            
            #first 7 columns, are always the same, make dict once
            if i <=6:#update this to be felxible $$
                outdict[keys]=dicts[keys]
                i+=1
            else:
                #copy of dict with first 7 columns of the df, then add the countries + status
                temp_outdict=copy.deepcopy(outdict)
                if dicts[keys]=="":
                    temp_outdict["Country"]=f"KEY_1_SHORT - {keys}"
                    temp_outdict["Status"]="Rollout to be determined"
                    temp_outdict["Start Date"]="tbd"
                    temp_outdict["End Date"]="tbd"
                    my_new_datadict.append(temp_outdict)
                    pass
                #exclude no rollout ones$$
                #
                elif dicts[keys]=="ø":
                    #temp_outdict["Country"]=f"KEY_1_SHORT - {keys}"
                    #temp_outdict["Status"]="No Rollout"
                    #temp_outdict["Start Date"]=""
                    #temp_outdict["End Date"]=""
                    #my_new_datadict.append(temp_outdict)
                    pass
                elif dicts[keys]=="√":
                    temp_outdict["Country"]=f"KEY_1_SHORT - {keys}"
                    temp_outdict["Status"]="Rollout Completed"
                    temp_outdict["Start Date"]=""
                    temp_outdict["End Date"]=""
                    my_new_datadict.append(temp_outdict)
                elif dicts[keys][:6]=="Start:":
                    temp_outdict["Country"]=f"KEY_1_SHORT - {keys}"
                    temp_outdict["Status"]="Rollout in Progress"

                    list_of_contents = dicts[keys].split()
                    my_dates = list_of_contents[1::2]
                    #Try Block, sometimes there are typos or only a start date without an end date.
                    #In that case just use blank start and end date instead of the programm stopping
                    try:
                        temp_outdict["Start Date"]=my_dates[0]
                        temp_outdict["End Date"]=my_dates[1]
                        my_new_datadict.append(temp_outdict)
                    except:
                        temp_outdict["Start Date"]=""
                        temp_outdict["End Date"]=""
                        my_new_datadict.append(temp_outdict) 
    
    #output_datadict=pd.DataFrame(data=my_new_datadict, dtype=object)
    #output_datadict=output_datadict.fillna("")
    #return output_datadict
    return my_new_datadict