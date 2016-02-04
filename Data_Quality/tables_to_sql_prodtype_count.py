'''
Created on Dec 1, 2015

@author: mstirling
'''
import pandas as pd

#folder data
in_folder = 'C:/Temp/python/in/'
in_file = 'MR_CTR_DQ_Rules v2 1 2015-12-03.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'tables_to_sql.txt'

DQ_Tables = pd.read_excel(in_folder + in_file,'All Table List', header = 0, parse_cols=7)

f_out = open(out_folder + out_file,'w')
for col_name in [u'Landing Tables']:
    for this_name in DQ_Tables[col_name]:
        #select 'BOND_L' as table_name, count (LINE_NUM) FROM CTRMSO.BOND_L
        if str(this_name) == 'nan':
            break
        #f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count FROM CTRMSO." + str(this_name) + '\n')
        f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count from (select distinct CTR_OBJECT_TYPE FROM CTRMSO." + str(this_name) + ') nest \n')

for col_name in [u'Extract Tables']:
    for this_name in DQ_Tables[col_name]:
        #select 'BOND_L' as table_name, count (LINE_NUM) FROM CTRMSO.BOND_L
        if str(this_name) == 'nan':
            break
        
        if str(this_name)[:10] == 'RISKWATCH_':
            f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count from (select distinct CTR_OBJECT_TYPE FROM CTRMSO." + str(this_name) + ') nest \n')
        elif str(this_name)[:10] == 'LANCELOT_TRADE_':
            f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count from (select distinct CTR_PRODUCT_TYPE FROM CTRMSO." + str(this_name) + ') nest \n')
        elif str(this_name)[:20] == 'LANCELOT_UNDERLYING_':
            f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count from (select distinct CTR_INSTRUMENT_TYPE FROM CTRMSO." + str(this_name) + ') nest \n')
        elif str(this_name)[:20] == 'LANCELOT_COLLATERAL_':
            f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count from (select distinct CTR_COLLATERAL_TYPE FROM CTRMSO." + str(this_name) + ') nest \n')
            
        #f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count FROM CTRMSO." + str(this_name) + '\n')
        #f_out.write("union select '" + str(this_name) + "' as table_name, count(*) as table_count from (select distinct CTR_PRODUCT_TYPE FROM CTRMSO." + str(this_name) + ') nest \n')


        
print ('done: ' + out_folder + out_file)



