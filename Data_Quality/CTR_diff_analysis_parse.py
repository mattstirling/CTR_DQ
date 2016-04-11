'''
Created on Jan 20, 2016

Inputs:
CTR Diff analysis from the CTR Data Arachitect. This compares the current CTR PRD data model vs. the previous CTR PRD data model.
List of tables in scope.

@author: mstirling
'''
import time

#control variables
bWriteReport = 1

#file variables
in_folder = 'C:/Temp/python/in/'
in_file = 'Comparison Summary V3_56 (L) vs V3.82 (R).txt'
in_file_table_list = 'CTR_table_list.txt'
out_folder = 'C:/Temp/python/out/'
out_file_table_list = in_file[:-4] + '_tables_' + time.strftime("%Y%m%d") + '.txt'
out_file_summary = in_file[:-4] + '_changes_' + time.strftime("%Y%m%d") + '.txt'

#tables to look for
table_list = []
for line in open(in_folder + in_file_table_list, 'r'):
    table_list.append(str(line).strip())
print table_list

#tables out    
f_table_out = open(out_folder + out_file_table_list, 'w')
f_summary_out = open(out_folder + out_file_summary, 'w')

#initialize control variables
b_include_this_table = 0
b_begin_writing = 0

#parse through diff analysis file
with open(in_folder + in_file, 'r') as this_in_file:
    line_count = 0
    for line in this_in_file:
        line_count+=1
        
        if '<Table>' in line:
            #check if this table is in scope
            b_include_this_table = 0
            #include BOND_L but not BOND_L_A
            if len([table for table in table_list if table in line])>0 and len([table for table in table_list if (table + '_A') in line])==0: 
                f_table_out.write(str(line_count) + ',' + line)
                b_include_this_table = 1 
                b_begin_writing = 1
    
        if b_include_this_table:
            if 'Columns' in line:b_begin_writing=1
            if '<Options>' in line or 'Indexes:' in line:b_begin_writing = 0
            
            if b_begin_writing: 
                f_summary_out.write(str(line_count) + ',' + line)

f_table_out.close()

print 'done.'  