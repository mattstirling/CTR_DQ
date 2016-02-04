'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd
import time

#control variables
bWriteReport = 1

#file variables
sFilePath = 'C:/Temp/python/in/MR_CTR_DQ_Rules v2 1 2015-12-03.xlsx'
destination = 'C:/Temp/python/out/'
out_folder = 'C:/Temp/python/out/'
out_file = 'report_DQ_BRD_rule_list_with_report_attributes_' + time.strftime("%Y%m%d") + '.xlsx'

#program variables
rule_col_list = ['isNotNull','isGreaterThan','isLessThan','amtIsLessThan','inDomain']
param_col_list = ['CURRENCY','START_DATE','VALUATION_DATE','MATURITY_DATE']
DQ_out = pd.DataFrame(columns=['CTR Table Name','CTR Table Filter','CTR Physical Column Name','DQ Rule Name','DQ Rule Parameters',
                               'CTR Rule Code','CDE Name','EDMO Rule Dimension','CBA Rule Dimension','DQ Rule Desc','DQ Rule Test Depth'])

#read rules from the BRD
DQ_xls = pd.read_excel(sFilePath,'DQ Rule List', header = 1)
DQ_Rule_Metadata = pd.read_excel(sFilePath,'DQ Rule Library List', header = 1)
print DQ_Rule_Metadata

for i in DQ_xls.index:
    
    #get 'mandatory attributes'
    this_tablename = DQ_xls.at[i,'CTR Table Name'] 
    this_filtername = DQ_xls.at[i,'CTR Table Filter']
    this_columnname = DQ_xls.at[i,'CTR Physical Column Name']
    this_CDE = DQ_xls.at[i,'CDE']
    
    #get filtername
    if str(this_filtername)=='nan':
        this_filtername = ''
    else:
        this_filtername = str(this_filtername)
    
    #get attributes of the rulename
    
    for rule in rule_col_list:
        if not str(DQ_xls.at[i,rule])=='nan':
            for rule_param in DQ_xls.at[i,rule].split('),'):
                
                #get the CTR rule code
                this_rule = rule
                this_parameter = str(rule_param + ')').replace('))', ')').strip() 
                for param in param_col_list:
                    this_parameter = this_parameter.replace(param,str(DQ_xls.at[i,param]))
                this_CTR_rulecode = (this_tablename + '.' + this_columnname + '.' + this_rule + this_parameter + ' ' + this_filtername).strip()
                
                #get the rule metadata
                #df_this_rule = DQ_Rule_Metadata.loc[DQ_Rule_Metadata['DQ Rule Name'] == this_rule].Index[0]
                this_rule_loc = DQ_Rule_Metadata.loc[DQ_Rule_Metadata['DQ Rule Name'] == this_rule].index.values[0]
                this_rule_dim_EDMO = DQ_Rule_Metadata.ix[this_rule_loc,'EDMO Dimension']
                this_rule_dim_CBA = DQ_Rule_Metadata.ix[this_rule_loc,'CBA Dimension']
                this_rule_desc = DQ_Rule_Metadata.ix[this_rule_loc,'Rule Description']
                this_rule_test_depth = DQ_Rule_Metadata.ix[this_rule_loc,'Rule Test Depth']
                
                DQ_out.loc[DQ_out.shape[0]+1] = [this_tablename, 
                                                this_filtername,
                                                this_columnname,
                                                this_rule,
                                                this_parameter,
                                                this_CTR_rulecode,
                                                this_CDE,
                                                this_rule_dim_EDMO,
                                                this_rule_dim_CBA,
                                                this_rule_desc,
                                                this_rule_test_depth
                                                ]
    
DQ_out.to_excel(pd.ExcelWriter(out_folder + out_file), sheet_name = 'DQ BRD Rule List', index = False)
    
        
print('done DQ_Rules_to_pivot')       
print out_folder+out_file

    