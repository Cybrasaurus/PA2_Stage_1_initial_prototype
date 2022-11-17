"""
        author: Adrian Scheubrein
        date: 25.01.2022
        version: 1.0.1
        license: MIT
"""
import pandas as pd
import re
import copy
import datetime




def date_format_converter_v2(pandas_datetime, OutName:str):
    """[This function convert a pandas timestamp (YYYY-MM-DD HH:MM:SS) to another date format (DD.MM.YYYY)]

    Args:
        pandas_datetime ([pandas_datetime]): [The pandas timestamp (YYYY-MM-DD HH:MM:SS) format]

    Returns:
        [datetime]: [the date in the (DD.MM.YYYY) format]
    """
    if OutName =="KEY_1_LONG Projekte":
        if pandas_datetime=="":
            out_date=""
        elif pandas_datetime=="tbd":
            out_date="tbd"
        else:
            splittime=pandas_datetime.split(".")
            myyear=splittime[2]
            mymonth=splittime[1]
            myday=splittime[0]
            myyear_int=int(myyear)
            mymonth_int=int(mymonth)
            myday_int=int(myday)
            out_date=datetime.date(year=myyear_int,month=mymonth_int,day=myday_int)
    elif OutName=="KEY_2_LONG Projekte":
        str_pd_datetime = str(pandas_datetime)
        myyear=str_pd_datetime[:4]
        mymonth=str_pd_datetime[5:7]
        myday=str_pd_datetime[8:10]


        combined_date=f"{myday} {mymonth} {myyear}"
        try:
            if combined_date != '  ':
                myyear_int=int(myyear)
                mymonth_int=int(mymonth)
                myday_int=int(myday)
                out_date=datetime.date(year=myyear_int,month=mymonth_int,day=myday_int)
                #print(out_date)
            else:
                out_date=""
        except ValueError:
            out_date=""
    else:
        if str(pandas_datetime)=="NaT":
            out_date=""
        else:
            str_pd_datetime = str(pandas_datetime)
            myyear=str_pd_datetime[:4]
            mymonth=str_pd_datetime[5:7]
            myday=str_pd_datetime[8:10]


            combined_date=f"{myday} {mymonth} {myyear}"
            if combined_date != '  ':
                myyear_int=int(myyear)
                mymonth_int=int(mymonth)
                myday_int=int(myday)
                out_date=datetime.date(year=myyear_int,month=mymonth_int,day=myday_int)
                #print(out_date)
            else:
                out_date=""
    return out_date

def doublesplitter(rawExcelData:list):
    """[This function creates multiple dictionaries based on a single dictionary from the raw Excel Data, if a field in the Column "Affected Division and Region" as multiple entries]

    Args:
        rawExcelData (list): [A list of Dictionaries, provided by the load_excel() function from data_get_raw]

    Returns:
        [list]: [A list of Dictionaries, without double entries in any field in the Column "Affected Division and Region"]
    """
    mylist=[]
    doublesList=[]
    i=0
    for dicts in rawExcelData:
        #make a list of dicts of the ones that contain doubles
        if "," in dicts["Affected Division and Region"]:
            for items in dicts["Affected Division and Region"].split(","):
                items=items.replace(" ", "").replace("-", " - ")
                tempdict=copy.deepcopy(dicts)
                tempdict["Affected Division and Region"]=items
                doublesList.append(tempdict)
        #make a list of dicts of the ones without doubles
        else:
            mylist.append(dicts)
    #combine the 2 lists again
    no_doubles_ExcelData=mylist+doublesList
    return no_doubles_ExcelData

def newDict_filler(configDict:dict, rawExcelData:list,cwd_path:str, OutName:str):
    """[This function creates the formatted pandas Dataframe based on the raw data from the excel, formatted according to the config file]

    Args:
        configDict (dict): [The Config File Data]
        rawExcelData (list): [The Raw Excel Data, a list of Dicts]
        OutName (str, optional): [The Name of the Output File of one step]

    Returns:
        [pandas dataframe]: [the formatted pandas dataframe]
    """
    
    #split rows that contain multiple countries into multiple rows

    if OutName=="Changes":
        no_doubles_ExcelData=doublesplitter(rawExcelData)
    else:
        no_doubles_ExcelData=rawExcelData

    #make an empty list to later convert back into a Pandas Dataframe
    outList = []

    #iterate through the Dictionaries of the rawExcelData List, effectively iterating through the rows of the excel
    for dicts in no_doubles_ExcelData:
        output_Dict = {}
        #iterate through the key-value pairs of the dictionary found in the config file
        for items in configDict:
            #cover the non-special cases, fill an empty dictionary with the Key from the config dict and the corresponding value from the excel
            if items[:10] != "-special- ":
                #convert the pandas timestamp (YYYY-MM-DD HH:MM:SS) to just the date (DD.MM.YYYY)
                if configDict[items] == "Start Date" or configDict[items] == "End Date":
                    #print(dicts)
                    formatted_date=date_format_converter_v2(dicts[items],OutName)
                    output_Dict[configDict[items]]=formatted_date
                else:
                    output_Dict[configDict[items]]=dicts[items]
            else:
                #use wildcard search for no raw data special cases, add a key-value pair to the dict, value is empty string
                if re.search("-special- no raw data .", items):
                    output_Dict[configDict[items]]=""
                #the taskletter export has 2 columns which are use to fill the end date column in the result sheet
                #if a taskletter is completed, use that date, if not use the due date
                #convert the pandas timestamp (YYYY-MM-DD HH:MM:SS) to just the date (DD.MM.YYYY)
                elif items == "-special- End Date":
                    if dicts["Completed"] != "":
                        formatted_date=date_format_converter_v2(dicts["Completed"],OutName)
                        output_Dict["End Date"]=formatted_date
                    else:
                        formatted_date=date_format_converter_v2(dicts["Due Date"],OutName)
                        output_Dict["End Date"]=formatted_date
                    #print(dicts["Completed"])
                #the Taskletter Export is formatted differently than the other exports, where Division and Region are seperate
                #columns, unlike the others, where it is combined. As such this is handled seperatly
                elif items=="-special- SENSITIVE DATA CENSORING":
                    curr_country=dicts["SENSITIVE DATA CENSORING"]
                    if dicts["SENSITIVE DATA CENSORING"]=="KEY_1_SHORT":
                        output_Dict["Affected SENSITIVE DATA CENSORING"]=f"KEY_1_SHORT - {curr_country}"
                        output_Dict["SENSITIVE DATA CENSORING"]="KEY_1_LONG"
                    elif dicts["SENSITIVE DATA CENSORING"]=="KEY_2_SHORT":
                        output_Dict["Affected SENSITIVE DATA CENSORING"]=f"KEY_2_SHORT - {curr_country}"
                        output_Dict["SENSITIVE DATA CENSORING"]="KEY_2_LONG"
                    elif dicts["SENSITIVE DATA CENSORING"]=="S":
                        output_Dict["Affected SENSITIVE DATA CENSORING"]=f"S - {curr_country}"
                        output_Dict["SENSITIVE DATA CENSORING"]="KEY_3_LONG"
                    elif dicts["SENSITIVE DATA CENSORING"]=="SP":
                        output_Dict["Affected SENSITIVE DATA CENSORING"]=f"SP - {curr_country}"
                        output_Dict["SENSITIVE DATA CENSORING"]="KEY_3_LONG SENSITIVE DATA CENSORING"
                #The Activity Subject Column of the Taskletter always begins with
                #Service Catalog Order: "TASKLETTER" (RITM*******) : 
                #which is irrelevant information, removing that here
                elif items=="-special- SENSITIVE DATA CENSORING":
                    shorter_subject=dicts["SENSITIVE DATA CENSORING"].split(") : ")[1]
                    output_Dict["Activity SENSITIVE DATA CENSORING"]=shorter_subject
                #manually set these 3 fields, are not supplied with the project raw data
                elif items=="-special- SENSITIVE DATA CENSORING":
                    output_Dict["SENSITIVE DATA CENSORING Type"]="SENSITIVE DATA CENSORING-Rollout"
                elif items=="-special- SENSITIVE DATA CENSORING KEY_2_SHORT":
                    output_Dict["SENSITIVE DATA CENSORING Type"]="SENSITIVE DATA CENSORING-Rollout"
                elif items=="-special- SENSITIVE DATA CENSORING KEY_2_SHORT project":
                    output_Dict["SENSITIVE DATA CENSORING"]="KEY_2_LONG"
                #manually add the "KEY_2_SHORT - " before the country in the KEY_2_SHORT projects
                elif items=="-special- SENSITIVE DATA CENSORING":
                    output_Dict["Affected SENSITIVE DATA CENSORING"]=f"KEY_2_SHORT - {dicts['Country']}"
        #Fill in the Division Column for Change Requests and Issues
        if output_Dict["SENSITIVE DATA CENSORING"]=="":
            if output_Dict["SENSITIVE DATA CENSORING"]=="":
                pass
            elif output_Dict["Affected SENSITIVE DATA CENSORING"].split(" - ")[0]=="KEY_1_SHORT":
                output_Dict["SENSITIVE DATA CENSORING"]="KEY_1_LONG"
            elif output_Dict["Affected SENSITIVE DATA CENSORING"].split(" - ")[0]=="S":
                output_Dict["SENSITIVE DATA CENSORING"]="KEY_3_LONG"
            elif output_Dict["Affected SENSITIVE DATA CENSORING"].split(" - ")[0]=="SP":
                output_Dict["SENSITIVE DATA CENSORING"]="KEY_3_LONG Produktion"
            elif output_Dict["Affected SENSITIVE DATA CENSORING"].split(" - ")[0]=="KEY_2_SHORT":
                output_Dict["SENSITIVE DATA CENSORING"]="KEY_2_LONG"
            elif output_Dict["Affected SENSITIVE DATA CENSORING"].split(" - ")[0]=="Z":
                output_Dict["SENSITIVE DATA CENSORING"]="Z"

        outList.append(output_Dict)
    #convert the list of dictionaries to a pandas dataframe
    endDF= pd.DataFrame(data=outList, dtype=object)
    endDF.to_excel(f"{cwd_path}/Results/Rename Konsol {OutName}.xlsx")
    print("done: ", OutName)
    return endDF
    
    
