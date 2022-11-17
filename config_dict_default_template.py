"""
        author: Adrian Scheubrein
        date: 18.01.2022
        version: 1.0.0
        license: MIT
"""
"""
[This Module contains the dictionaries which contain the default settings on how the Excels with
the raw data get read and then used for the combined Output File.

*my_dict_filenames
    This Dictionary contains the names of the raw data files that get read to build the output


*my_dict_changes,my_dict_issues,my_dict_tasks
    The dictionary Key Represents the column header in raw data excel, the corresponding value contains
    name of the column in the combined Output File, with the following exceptions:

    Any key that starts with '-special-' gets handled differently
        -"no raw data *": A empty column is generated in the output file
        -"-special- End Date": This is a unique case. End Date is the column name in the output file, 
            "Due Date" and "Completed" are the columns in the raw data. If a "completed" value exists,
            that is the value that gets put into the "End Date" Column on the output file, if there is
            no value in "Completed", the value from "Due Date" gets used instead
 ]
"""


my_dict_filenames = {
    "raw_excel_changes":"change_request",
    "raw_excel_issues":"sn_grc_issue (1)",
    "raw_excel_taskletter":"u_request_task"

}
#Dictionary for the Changes Raw Data
my_dict_changes = {
    "SENSITIVE DATA CENSORING":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 1":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 2":"SENSITIVE DATA CENSORING",
    "Planned start date":"Start Date",
    "Planned end date":"End Date",
    "SENSITIVE DATA CENSORING 3":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 4":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 5":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 6":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 7":"SENSITIVE DATA CENSORING",
    "-special- no raw data 0":"SENSITIVE DATA CENSORING",
    "-special- no raw data 1":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 8":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 9":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 10":"SENSITIVE DATA CENSORING",
    "-special- no raw data 2":"SENSITIVE DATA CENSORING",
    "Updated at":"Updated At",

}
#Dictionary for the Issues Raw Data
my_dict_issues = {
    "SENSITIVE DATA CENSORING":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 1":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 2":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 3":"SENSITIVE DATA CENSORING",
    "Planned End date":"End Date",
    "SENSITIVE DATA CENSORING 4":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 5":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 6":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 7":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 8":"SENSITIVE DATA CENSORING",
    "-special- no raw data 0":"SENSITIVE DATA CENSORING",
    "-special- no raw data 1":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 9":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 10":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 11":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 12":"SENSITIVE DATA CENSORING",
    "Updated at":"Updated At"
}
#Dictionary for the Taskletter Raw Data
my_dict_tasks = {
    "SENSITIVE DATA CENSORING":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 1":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 2":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 3":"SENSITIVE DATA CENSORING",
    "-special- End Date":["Due Date","Completed"],
    "SENSITIVE DATA CENSORING 4":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 5":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 6":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 7":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 8":"SENSITIVE DATA CENSORING",
    "-special- no raw data 0":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 9":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 10":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 11":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 12":"SENSITIVE DATA CENSORING",
    "SENSITIVE DATA CENSORING 13":"SENSITIVE DATA CENSORING",
    "Updated at":"Updated At"
}
#List containing all the dictionaries
my_dict_list = [my_dict_filenames,my_dict_changes,my_dict_issues,my_dict_tasks]