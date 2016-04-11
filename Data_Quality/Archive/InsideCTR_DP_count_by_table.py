'''
Created on Jan 7, 2016

@author: mstirling
'''

import cx_Oracle, time
#import os

in_folder = 'C:/Temp/python/in/'
in_file = 'table_list.txt'
in_file_connection = 'Ref Data/CTR_PRD_connection.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'table_list_RecordCount_' + time.strftime("%Y%m%d") + '.csv'

#open vm db connecttion - connection string stored in txt 
f_in_connection_string = open(in_folder + in_file_connection,'r')
connection_string = str(f_in_connection_string.readline().strip())
conn = cx_Oracle.connect(connection_string)    
cursor = conn.cursor ()  
f_out = open(out_folder+out_file,'w')
f_out.write('table,total_count' + '\n')

for line in open(in_folder+in_file,'r'):
    table = line.strip()
    
    #get count of all records in table
    sql_for_total_cnt = 'select count(*) from CTRMSO.' + str(table)
    print sql_for_total_cnt
    total_count = cursor.execute(sql_for_total_cnt).fetchall()[0][0]
    #total_count = this_cursor.fetall()[0][0]
    
    f_out.write(table)
    f_out.write(','+str(total_count))
    f_out.write('\n')

#close connection
cursor.close () 
conn.close ()

#report done
print 'done, ' + str(in_folder) + str(in_file) + ' to ' + str(out_folder) + str(out_file)
