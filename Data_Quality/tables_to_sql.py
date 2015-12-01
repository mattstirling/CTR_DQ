'''
Created on Dec 1, 2015

@author: mstirling
'''
import pandas as pd

#folder data
in_folder = 'C:/Temp/python/in/'
in_file = 'MR_CTR_DQ_Rules v0 10 2015-11-27.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'tables_to_sql.txt'

DQ_Tables = pd.read_excel(in_folder + in_file,'All Table List', header = 0, parse_cols=7)

f_out = open(out_folder + out_file,'w')
for col_name in [u'Landing Tables', u'Extract Tables']:
    for this_name in DQ_Tables[col_name]:
        #select 'BOND_L' as table_name, count (LINE_NUM) FROM CTRMSO.BOND_L
        if str(this_name) == 'nan':
            break
        f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count FROM CTRMSO." + str(this_name) + '\n')
print ('done: ' + out_folder + out_file)



