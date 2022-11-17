"""
        author: Adrian Scheubrein
        date: 18.01.2022
        version: 1.0.0
        license: MIT
"""
import config_handling  as my_ch
import pandas as pd
import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
import os


def nan_replacer(input_df):
    """[This Function replaces the NAN and NAT values in a pandas dataframe with blank values]

    Args:
        input_df ([pandas dataframe]): [The Pandas Dataframe from which NAN/NAT values are to be removed]

    Returns:
        [pandas dataframe]: [The cleaned pandas dataframe]
    """
    output_df = input_df.fillna("")
    return output_df



def load_excel(excel_to_load:str, cwd_path:str):
    """[This function loads the contents of an excel file as a pandas dataframe and returns it]

    Args:
        excel_to_load (str): [The Key of the Key-Value Pair found in the config Dictionary "my_dict_filenames"]

    Returns:
        [List of Dictionaries]: [The Contents of the Excel File as a pandas Dataframe, converted to a list of dictionaries]
    """
    try:
        #get a dictionary of the the excel file names containing the raw data
        excel_name_dict=my_ch.read_config(cwd_path=cwd_path)[0]
        #get the file name of the excel containing the raw data
        excel_file_name=excel_name_dict[excel_to_load]
        #load the contents of the excel as a pandas dataframe and return it
        loaded_df = pd.read_excel(f"{cwd_path}/Raw_Excels/{excel_file_name}.xlsx")
        #replace nan values with blanks
        loaded_df=nan_replacer(loaded_df)
        #return loaded_df
        my_dataDictList = loaded_df.to_dict("records")
        return my_dataDictList
    except KeyError:
        logging.debug("get_raw_data load_excel -- Invalid Key for Dictionary")
    except FileNotFoundError:
        logging.debug("get_raw_data load_excel -- Could not find File or Directory. Please double check if the raw excels are in the correct folder and the config has the right names")
    
    


def get_project_and_id():
    cwd=os.getcwd()
    cwd=cwd.replace("\\", "/")
    mydatadict=load_excel("raw_excel_projecteUndID",cwd)
    projectAndID_df= pd.DataFrame(data=mydatadict, dtype=object)
    projectAndID_df=projectAndID_df.iloc[:,[1,2,4]]
    projectAndID_datadict=projectAndID_df.to_dict("records")
    return projectAndID_datadict