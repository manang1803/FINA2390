# -*- coding: utf-8 -*-
"""
@author: gupta
"""
import pandas as pd
from datetime import datetime as dt
a = dt.now()
df = pd.read_csv(r"C:\Users\gupta\Documents\FINA2390\Data Transformation\Data Transformation\deal_level_data.csv")

df = df.drop(df.columns[541:1019], axis=1) #to reduce size of dataframe
df = df.drop(df.columns[-47], axis = 1)

col = ['Deal_Number', 'Date_Announced', 'Year_Announced', 'Acquirer_Name_clean', 'Acquirer_Primary_SIC', 'Acquirer_State_abbr',
       'Acquirer_CUSIP', 'Acquirer_Ticker', 'Target_Name_clean',
       'Target_Primary_SIC', 'Target_State_abbr', 'Target_CUSIP',
       'Target_Ticker', 'Attitude', 'quarter_to_the_event_date', 'quarter',
       'Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII',
       'Com_NIM', 'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary',
       'Com_EmployNum', 'Com_TtlSalary', 'Com_AvgSalary_log',
       'Com_EmployNum_log', 'Com_TtlSalary_log', 'Tar_Net_Charge_Off',
       'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM', 'Tar_ROA',
       'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
       'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']#all columns in the quarter level data

col_needed = ['quarter','Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', 'Com_NII',
       'Com_NIM', 'Com_ROA', 'Com_Total_Assets', 'Com_AvgSalary',
       'Com_EmployNum', 'Com_TtlSalary', 'Com_AvgSalary_log',
       'Com_EmployNum_log', 'Com_TtlSalary_log', 'Tar_Net_Charge_Off',
       'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', 'Tar_NIM', 'Tar_ROA',
       'Tar_Total_Assets', 'Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',
       'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log'] #these have the underscroes infront of them

tempdic = {el:[] for el in col}

count = 0 #for keeping count of len(df)

df2 = pd.DataFrame(columns = col)
df_a_temp = df[df.columns[:14]]

for x in range(len(df)):
    df_a = df_a_temp.loc[x]
    q_val = -12
    q_date = 12
    for i in range(25):
        for j in range(14):
            tempdic[col[j]].append(df_a[col[j]])
            
        tempdic["quarter_to_the_event_date"].append(i-12)
        
        if q_val<0:
            for col1 in col_needed:
                tempdic[col1].append(df[col1+"__"+str(q_date)][x])
            q_date -= 1
            
        elif q_val == 0:
            for col1 in col_needed:
                tempdic[col1].append(df[col1][x])
            q_date = 1    
    
        else:
            for col1 in col_needed:
                tempdic[col1].append(df[col1+"_"+str(q_date)][x])
            q_date += 1 
         
        q_val += 1
       
df2 = pd.DataFrame({key:pd.Series(value) for key, value in tempdic.items()})

df2.to_csv(r"C:\Users\gupta\Documents\FINA2390\Data Transformation\final_output_quarter_level.csv", index = False)
b= dt.now()
print(b-a)

