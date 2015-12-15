'''
Created on Dec 1, 2015

@author: mstirling
'''
#folder data
in_folder = 'C:/Temp/python/in/'
in_file = 'table_list.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'comma_table_list.txt'

f_out = open(out_folder + out_file,'w')
   
for line in open(in_folder + in_file,'r'):
    for name in line.strip().split(','):
        f_out.write(name.upper().replace('CTRMSO.',''))
        f_out.write('\n')
        
f_out.close()

print 'done : ' + out_folder + out_file
