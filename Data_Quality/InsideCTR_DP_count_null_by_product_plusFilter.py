'''
Created on Jan 7, 2016

@author: mstirling
'''

import cx_Oracle,os,pandas as pd,time

in_folder = 'C:/Temp/python/in/'
in_file = 'table_col_filter_list.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'table_col_filter_list_NullCount_' + time.strftime("%Y%m%d") + '.xlsx'

#open vm db connecttion  
#conn = cx_Oracle.connect('CTRMSO/password@localhost:1522/orcl')    
conn = cx_Oracle.connect('CTR_READ_ONLY/MGJahCLu#7@//sgdxwa01-scan.bns:1535/CTRu1_sgdxwa01.bns')    
cursor = conn.cursor ()  

df_xls = pd.read_excel(in_folder + in_file,'table_col_filter_list', header = 0)
df_out = pd.DataFrame(columns=['Table','Col','Table Filter','Nonnull Count','Record Count'])

for i in df_xls.index:
    table = str(df_xls.at[i,'Table']) 
    col = str(df_xls.at[i,'Col']) 
    table_filter = str(df_xls.at[i,'Table Filter']) 
    
    #stop if table is nan
    if table == 'nan': break
    
    #remove the 'nan' table_filter values
    if table_filter == 'nan': table_filter = ''
    
    #get nonnull count for this column
    sql_for_nonnull_cnt = 'select count(' + str(col) + ') from CTRMSO.' + str(table) + str(table_filter)
    #print sql_for_nonnull_cnt
    nonnull_count = cursor.execute(sql_for_nonnull_cnt).fetchall()[0][0]
    
    #get count of all records in table
    sql_for_total_cnt = 'select count(*) from CTRMSO.' + str(table) + str(table_filter)
    #print sql_for_total_cnt
    total_count = cursor.execute(sql_for_total_cnt).fetchall()[0][0]
    
    #store record in dataframe
    df_out.loc[df_out.shape[0]+1] = [table, 
                                    col,
                                    table_filter,
                                    nonnull_count,
                                    total_count]


#close connection
cursor.close () 
conn.close ()  

#write to xls
df_out.to_excel(pd.ExcelWriter(out_folder + out_file), sheet_name = 'table_col_filter_list', index = False)

#report done
print 'done, ' + str(in_folder) + str(in_file) + ' to ' + str(out_folder) + str(out_file)
