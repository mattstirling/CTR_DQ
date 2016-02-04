'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd
import time

bWriteReport = 1

in_folder = 'C:/Temp/python/in/'
in_file = 'MR_CTR_DQ_Rules_v3_0__2016-01-08.xlsx'
in_map_file = 'RuleMap CTR_BRD to IA_DEV 20151231.xlsx'
destination = 'C:/Temp/python/out/'
out_folder = 'C:/Temp/python/out/'
out_file = 'report_DQ_BRD_rule_list_' + time.strftime("%Y%m%d") + '.xlsx'

DQ_xls = pd.read_excel(in_folder + in_file,'DQ Rule Matrix', header = 1)
DQ_RuleMap = pd.read_excel(in_folder + in_map_file,'Rule Map')
rule_col_list = ['isNotNull','isGreaterThan','isLessThan','amtIsLessThan','inDomain']
param_col_list = ['CURRENCY','START_DATE','VALUATION_DATE','MATURITY_DATE']
DQ_out = pd.DataFrame(columns=['CTR Table Name','CTR Table Filter','CTR Physical Column Name','DQ Rule Name','DQ Rule Parameters','CTR Rule Code'])

for i in DQ_xls.index:
    
    '''
    sTemp = ''
    if not pd.isnull(DQ_Rules[u'DQ Rule Name'][i]):
        sTemp = "[" + str(int(DQ_Rules[u'CTR DQ Rule Id'][i])) + "]"
        if not pd.isnull(DQ_Rules[u'CTR Table Filter'][i]):
            sTemp += "[" + str(DQ_Rules[u'CTR Table Filter'][i]) + "]"
        sTemp += str(DQ_Rules[u'CTR Physical Column Name'][i]) + "." + str(DQ_Rules[u'DQ Rule Name'][i]) + str(DQ_Rules[u'DQ Rule Metadata'][i])
    aTemp.append(sTemp)
    '''
    this_tablename = DQ_xls.at[i,'CTR Table Name'] 
    this_filtername = DQ_xls.at[i,'CTR Table Filter']
    this_columnname = DQ_xls.at[i,'CTR Physical Column Name']
    
    if str(this_filtername)=='nan':
        this_filtername = ''
        this_filtername_for_rulecode = '' 
    else:
        this_filtername = str(this_filtername)
        #this_filtername_for_rulecode = '[' +str(this_filtername)+']'
        #this_filtername_for_rulecode = ' ' + this_filtername +' for table ' + this_tablename
        this_filtername_for_rulecode = ' ' + this_filtername
    
    for rule in rule_col_list:
        if not str(DQ_xls.at[i,rule])=='nan':
            for rule_param in DQ_xls.at[i,rule].split('),'):
                this_rule = rule
                this_parameter = str(rule_param + ")").replace('))', ')').strip() 
                for param in param_col_list:
                    this_parameter = this_parameter.replace(param,str(DQ_xls.at[i,param]))
                this_CTR_rulecode = this_tablename + '.' + this_columnname + '.' + this_rule + this_parameter + this_filtername_for_rulecode
                
                DQ_out.loc[DQ_out.shape[0]+1] = [this_tablename, 
                                                this_filtername,
                                                this_columnname,
                                                this_rule,
                                                this_parameter,
                                                this_CTR_rulecode]
    
#outer-join the IA RuleCode to the CTR RuleCode
DQ_out = pd.merge(DQ_out,DQ_RuleMap,how='left',on=[u'CTR Rule Code'])

#write to Excel
DQ_out.to_excel(pd.ExcelWriter(out_folder + out_file), sheet_name = 'DQ BRD Rule List', index = False)
    
        
print('done DQ_Rules_to_pivot')       
print out_folder+out_file

    