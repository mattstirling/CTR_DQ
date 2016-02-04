'''
Created on Jan 7, 2016

@author: mstirling
'''

import cx_Oracle,os, time

in_folder = 'C:/Temp/python/in/'
in_file = 'table_list.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'table_list_RecordCount_' + time.strftime("%Y%m%d") + '.csv'

#open vm db connecttion  
#conn = cx_Oracle.connect('CTRMSO/password@localhost:1522/orcl')    
conn = cx_Oracle.connect('CTR_READ_ONLY/MGJahCLu#7@//sgdxwa01-scan.bns:1535/CTRu1_sgdxwa01.bns')    
#MGJahCLu#7
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
