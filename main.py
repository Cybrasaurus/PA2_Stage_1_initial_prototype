"""
        author: Adrian Scheubrein
        date: 18.01.2022
        version: 1.0.1
        license: MIT
"""

print("Started")
import data_process_raw as my_dpr
import config_handling as my_ch
import data_get_raw as my_dgr
import excel_handling as my_eh
import os
import data_process_KEY_1_LONGProjekte as my_dplP
import data_process_KEY_2_SHORTProjekte as my_dpkP
import time

#try:
#get Path to current working directory
cwd=os.getcwd()
cwd=cwd.replace("\\", "/")
print(cwd)

#Read the config File
configData=my_ch.read_config(cwd_path=cwd)


#generate the Pandas Dataframe for the Changes
change_df=my_dpr.newDict_filler(  configDict=configData[1],
                        rawExcelData=my_dgr.load_excel("raw_excel_changes", cwd_path=cwd),
                        OutName="Changes",
                        cwd_path=cwd
                        )
#generate the Pandas Dataframe for the Issues
issue_df=my_dpr.newDict_filler(  configDict=configData[2],
                        rawExcelData=my_dgr.load_excel("raw_excel_issues", cwd_path=cwd),
                        OutName="Issues",
                        cwd_path=cwd)
#generate the Pandas Dataframe for the Taskletter
task_df=my_dpr.newDict_filler(  configDict=configData[3],
                        rawExcelData=my_dgr.load_excel("raw_excel_taskletter", cwd_path=cwd),
                        OutName="Taskletter",
                        cwd_path=cwd)

#generate the Pandas Dataframe for the KEY_1_LONG Projects
KEY_1_LONGproj_df=my_dpr.newDict_filler(  configDict=configData[4],
                        rawExcelData=my_dplP.dictsorter(my_dplP.clean_raw_excel("raw_excel_KEY_1_LONGProjekte", cwd_path=cwd)),
                        OutName="KEY_1_LONG Projekte",
                        cwd_path=cwd)

#generate the Pandas Dataframe for the KEY_2_LONG Projects
KEY_2_SHORTproj_df=my_dpr.newDict_filler(  configDict=configData[5],
                        rawExcelData=my_dpkP.rawdatacleaner(excel_to_load="raw_excel_KEY_2_SHORTProjekte",cwd_path=cwd),
                        OutName="KEY_2_LONG Projekte",
                        cwd_path=cwd)

#generate the combined Pandas Dataframe, export it to an Excel
list_of_df=[change_df, issue_df, task_df, KEY_1_LONGproj_df,KEY_2_SHORTproj_df]
my_eh.make_excel_table(list_of_DF=list_of_df, cwd_path=cwd)

print("finished, excels are generated")

#except:
#        my_input=input("There was an error, check the console. Either close the console type 'ok' to confirm: ")
#        print(my_input)
    

