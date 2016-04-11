'''
Created on Mar 14, 2016

@author: mstirling
'''
#import
import pandas as pd, cx_Oracle, time

#
# SQL for counting "num not null records"
# challenge is that this SQL is different for date vs number columns
# 
def get_sql_for_nonnull_cnt(table, col):
    #depending on the col variable type, nonnull is a different function
    return (
        "select sum(Not_Null_Flag) from" 
       + " (select case when a." + col + " is null then 0"
       + " else 1 end Not_Null_Flag"
       + " from " + table + " a" 
       + " )")


def get_sql_for_total_cnt(table):
    return ("select count(*)" 
           + " from " + table + " a")

#
# Begin Program
#

#file variables
in_folder = 'C:/Temp/python/in/'
in_file = 'CTR_table_list.txt'
in_file_DQ_Rules = 'MR_CTR_DQ_Rules_v3_8__2016-02-22.xlsx'
in_file_connection = 'Ref Data/CTR_VM3_connection.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'out_CTR_table_nonnull_count_' + time.strftime("%Y%m%d") + '.xlsx'

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
print_cols = ['CTR Table Name', 'Column Id', 'CTR Physical Column Name', 'Nonnull Pct']

#for every xls
for line in f_in:
    print line.strip()
    tablename = line.strip()
    
    #get the list of all physical columns by using sql
    df_xls = pd.DataFrame(columns = ['CTR Table Name', 'Column Id', 'CTR Physical Column Name', 'Nonnull Pct'])
    
    sql = ('select table_name, column_id, column_name ' + 
           'from all_tab_columns ' +
           "where table_name = '" + tablename + "'" +
           'order by table_name, column_id, column_name') 
    
    result = cursor.execute(sql).fetchall()
    
    #load results into dataframe
    for i in result:
        
        this_col = i[2]
        
        #merge the current CDE and CTR Table Filter
        sql_for_nonnull_cnt = get_sql_for_nonnull_cnt(tablename, this_col)
        nonnull_count = cursor.execute(sql_for_nonnull_cnt).fetchall()[0][0]
        
        #get count of all records in table
        sql_for_total_cnt = get_sql_for_total_cnt(tablename)
        total_count = cursor.execute(sql_for_total_cnt).fetchall()[0][0]
        
        #write nonnull / total as a pct
        if total_count == 0: 
            this_summary = '0.0 (0 / 0)'
        else: 
            this_summary = "%.1f" % (100*float(nonnull_count)/float(total_count)) +' (' + str(nonnull_count) + ' / ' + str(total_count) + ')'
        
        df_xls.loc[df_xls.shape[0]+1] = i + (this_summary,)
        
    df_xls.to_excel(f_out, sheet_name = str(tablename), index = False, columns = print_cols)
        
    
print 'done'
print 'in from: ' + in_folder + in_file
print 'out to: ' + out_folder + out_file 