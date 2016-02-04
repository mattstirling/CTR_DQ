'''
Created on Jan 7, 2016

@author: mstirling
'''

import cx_Oracle,pandas as pd,time

in_folder = 'C:/Temp/python/in/'
in_file = 'table_col_filter_list.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'table_col_Byfilter_list_NullCount_' + time.strftime("%Y%m%d") + '.xlsx'

#open vm db connecttion  
conn = cx_Oracle.connect('CTRMSO/password@localhost:1522/orcl')    
cursor = conn.cursor ()  

df_xls = pd.read_excel(in_folder + in_file,'table_col_byFilter_list', header = 0)
df_out = pd.DataFrame(columns=['Table','Col','Table Filter Name','Nonnull Count','Record Count','Summary'])

for i in df_xls.index:
    table = str(df_xls.at[i,'Table']) 
    col = str(df_xls.at[i,'Col']) 
    
    if table == 'nan': break
    
    for j in df_xls.index:
        table_filter_name = str(df_xls.at[j,'Table Filter Name'])
        table_filter = str(df_xls.at[j,'Table Filter']) 
        
        #get nonnull count for this column
        sql_for_nonnull_cnt = 'select count(' + col + ') from ' + table + table_filter
        nonnull_count = cursor.execute(sql_for_nonnull_cnt).fetchall()[0][0]
        
        #get count of all records in table
        sql_for_total_cnt = 'select count(*) from ' + table + table_filter
        total_count = cursor.execute(sql_for_total_cnt).fetchall()[0][0]
        
        this_summary = "%.1f" % (100*float(nonnull_count)/float(total_count)) +' (' + str(nonnull_count) + ' / ' + str(total_count) + ')' 
        
        #store record in dataframe
        df_out.loc[df_out.shape[0]+1] = [table, 
                                        col,
                                        table_filter_name,
                                        nonnull_count,
                                        total_count,
                                        this_summary]


#close connection
cursor.close () 
conn.close ()  

#pivot df_out
df_pivot=pd.pivot_table(df_out,index=['Table Filter Name'],values=['Summary'],
               columns=['Table','Col'],aggfunc=lambda x: "%s" % ''.join(x),fill_value='')

#write to xls
with pd.ExcelWriter(out_folder + out_file) as writer:
    df_out.to_excel(writer, sheet_name = 'table_col_Byfilter_list', index = False)
    df_pivot.to_excel(writer, sheet_name = 'pivot', index = True, merge_cells = False)

#report done
print 'done, ' + str(in_folder) + str(in_file) + ' to ' + str(out_folder) + str(out_file)
