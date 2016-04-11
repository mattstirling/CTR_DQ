'''
Created on Dec 1, 2015

@author: mstirling
'''
import pandas as pd

b_addCTRMSO_to_table = 1

#folder data
in_folder = 'C:/Temp/python/in/'
in_file = 'MR_CTR_DQ_Rules_v3_3__2016-01-22.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'sql_table_system_count.txt'

df_tables = pd.read_excel(in_folder + in_file,'CTR Table List', header = 0)
f_out = open(out_folder + out_file,'w')

if b_addCTRMSO_to_table: 
    table_owner = 'CTRMSO.'
else:
    table_owner = '' 

for i in df_tables.index:
    
    this_source_col = str(df_tables.at[i,u'Source System Identifier'])
        
    if not this_source_col.upper() == '[N/A]':
        
        this_table = str(df_tables.at[i,u'CTR Table Name'])
        
        this_sql = ("union select '"
                    + this_table 
                    + "' as Table_Name,Source, Source_Count from (select Source, count(Source) as Source_Count from (select "
                    + this_source_col 
                    + " as Source from "
                    + table_owner
                    + this_table 
                    + ") group by source order by source)")
        
        f_out.write(this_sql)
        f_out.write('\n')
    
    
print ('wrote from: ' + in_folder + in_file)
print ('wrote to: ' + out_folder + out_file)
print ('done')



