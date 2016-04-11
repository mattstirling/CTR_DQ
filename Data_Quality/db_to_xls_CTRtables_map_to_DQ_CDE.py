'''
Created on Mar 14, 2016

@author: mstirling
'''
import pandas as pd, cx_Oracle, time

#file variables
in_folder = 'C:/Temp/python/in/'
in_file = 'CTR_table_list.txt'
in_file_DQ_Rules = 'MR_CTR_DQ_Rules_v3_8__2016-02-22.xlsx'
in_file_connection = 'Ref Data/CTR_VM3_connection.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'out_CTR_table_list_' + time.strftime("%Y%m%d") + '.xlsx'

#open file with table names in a list
f_in = open(in_folder + in_file,'r')
f_out = pd.ExcelWriter(out_folder + out_file)
df_DQ = pd.read_excel(in_folder + in_file_DQ_Rules,'DQ Rule Matrix', header = 1, parse_cols=4)

#open vm db connecttion  
f_in_connection_string = open(in_folder + in_file_connection,'r')
connection_string = str(f_in_connection_string.readline().strip())
conn = cx_Oracle.connect(connection_string)    
cursor = conn.cursor ()  

#print cols
print_cols = ['CTR Table Name', 'Column Id', 'CTR Physical Column Name','CDE','CTR Table Filter']

#for every xls
for line in f_in:
    print line.strip()
    tablename = line.strip()
    
    #get the list of all physical columns by using sql
    df_xls = pd.DataFrame(columns = ['CTR Table Name', 'Column Id', 'CTR Physical Column Name'])
    
    sql = ('select table_name, column_id, column_name ' + 
           'from all_tab_columns ' +
           "where table_name = '" + tablename + "'" +
           'order by table_name, column_id, column_name') 
    
    result = cursor.execute(sql).fetchall()
    
    #load results into dataframe
    for i in result:
        df_xls.loc[df_xls.shape[0]+1] = i
    
    #merge the current CDE and CTR Table Filter
    df_xls = pd.merge(df_xls,df_DQ, how='left',on=['CTR Table Name','CTR Physical Column Name'])
    
    df_xls.to_excel(f_out, sheet_name = str(tablename), index = False, columns = print_cols)
        
    
print 'done'
print 'in from: ' + in_folder + in_file
print 'out to: ' + out_folder + out_file 