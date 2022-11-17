"""
        author: Adrian Scheubrein
        date: 18.01.2022
        version: 1.0.0
        license: MIT
"""
import pandas as pd

def make_excel_table(list_of_DF, cwd_path):
    """[This Function combines the 3 input Pandas Dataframes into 1 with the concat function. It then writes the combined DF to excel and formats it as an Excel Table]

    Args:
        change_df (pd df): [The first pandas dataframe]
        issue_df (pd df): [The second pandas dataframe]
        task_df (pd df): [The third pandas dataframe]
    """
    #combine the 3 seperate dataframes into one big one
    dataFrames_combined = pd.concat(list_of_DF)

    #$$add date thing here to not overwrite the old version each time
    writer = pd.ExcelWriter(f'{cwd_path}/Results/Konsolidierte Gesamtübersicht Excel.xlsx', engine='xlsxwriter')
    dataFrames_combined.to_excel(writer, sheet_name='Rohdaten', startrow=1, header=False, index=False)

    workbook = writer.book
    worksheet = writer.sheets['Rohdaten']

    (max_row, max_col) = dataFrames_combined.shape
    column_settings = [{'header': column} for column in dataFrames_combined.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings,"name":"Rohdaten"},)

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()