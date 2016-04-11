'''
Created on Mar 14, 2016

@author: mstirling
'''
import pandas as pd, cx_Oracle, time

#file variables
in_folder = 'C:/Temp/python/in/'
in_file = 'CTR_table_list.txt'
in_file_connection = 'Ref Data/CTR_VM3_connection.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'out_CTR_table_list.xlsx'

#open file with table names in a list
f_in = open(in_folder + in_file,'r')
f_out = pd.ExcelWriter(out_folder + out_file)
df_DQ = pd.read_excel(sFilePath,'CDE List', header = 0, parse_cols=7)

#open vm db connecttion  
f_in_connection_string = open(in_folder + in_file_connection,'r')
connection_string = str(f_in_connection_string.readline().strip())
conn = cx_Oracle.connect(connection_string)    
cursor = conn.cursor ()  

#for every xls
for line in f_in:
    print line.strip()
    tablename = line.strip()
        
    df_xls = pd.DataFrame(columns = ['table_name', 'column_id', 'column_name'])
    
    sql = ('select table_name, column_id, column_name ' + 
           'from all_tab_columns ' +
           "where table_name = '" + tablename + "'" +
           'order by table_name, column_id, column_name') 
    
    result = cursor.execute(sql).fetchall()
    
    for i in result:
        df_xls.loc[df_xls.shape[0]+1] = i
    
    df_xls.to_excel(f_out, sheet_name = str(tablename), index = False)
        
    
print 'done'
print 'in from: ' + in_folder + in_file
print 'out to: ' + out_folder + out_file 