'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd
import time

bWriteReport = 1

in_folder = 'C:/Temp/python/in/'
in_file = 'MR_CTR_DQ_Rules_v3_7__2016-02-22.xlsx'
in_map_file = 'RuleMap CTR_BRD to IA_DEV 20151231.xlsx'
destination = 'C:/Temp/python/out/'
out_folder = 'C:/Temp/python/out/'
out_file = 'report_IA_rule_list_' + time.strftime("%Y%m%d") + '.xlsx'

#open data from xls
DQ_xls = pd.read_excel(in_folder + in_file,'DQ Rule Matrix', header = 1)
DQ_RuleLibrary = pd.read_excel(in_folder + in_file,'DQ Rule Library List', header = 1)
DQ_RuleMap = pd.read_excel(in_folder + in_map_file,'Rule Map')

#create hard-coded lists
rule_col_list = ['isNotNull','isDate','isValidRegex','isGreaterThan','isLessThan','amtIsLessThan','inDomain']
param_col_list = ['CURRENCY','REGEX','DATE_FORMAT','START_DATE','VALUATION_DATE','MATURITY_DATE']
rename_list = [['IA Rule Code','DQ_RULE_NM'],
            ['CDE','CDE_NAME'],
            ['CTR Physical Column Name','ATTRIBUTE_NAME'],
            ['EDMO Dimension','DQ_RULE_DIMENSION_EDMO'],
            ['CBA Dimension','DQ_RULE_DIMENSION_CBA'],
            ['Rule Description','DQ_RULE_DESCP'],
            ['Rule Test Depth','DQ_RULE_TST_DEPTH']]
hardcoded_value_list = [['DQ_RULE_TYPE_CD','BUSINESS'],
            ['DQ_RULE_LOGIC','[n/a]'],
            ['DQ_RULE_DEFAULT_FLAG','[n/a]'],
            ['DQ_RULE_SEVERITY','1'],
            ['POLICY_NAME','[n/a]'],
            ['POPULATION_DATE','[n/a]']]
out_cols = ['CTR Rule Code',
        'DQ_RULE_NM',
        'CDE_NAME',
        'ATTRIBUTE_NAME',
        'DQ_RULE_DIMENSION_EDMO',
        'DQ_RULE_DIMENSION_CBA',
        'DQ_RULE_TYPE_CD',
        'DQ_RULE_DESCP',
        'DQ_RULE_LOGIC',
        'DQ_RULE_DEFAULT_FLAG',
        'DQ_RULE_TST_DEPTH',
        'DQ_RULE_SEVERITY',
        'POLICY_NAME',
        'POPULATION_DATE',
        'Version']

#create output dataframe
DQ_out = pd.DataFrame(columns=['CTR Table Name','CTR Table Filter','CTR Physical Column Name','DQ Rule Name','DQ Rule Parameters','CTR Rule Code','CDE', 'Version'])

for i in DQ_xls.index:
    
    this_tablename = DQ_xls.at[i,'CTR Table Name'] 
    this_filtername = DQ_xls.at[i,'CTR Table Filter']
    this_columnname = DQ_xls.at[i,'CTR Physical Column Name']
    this_CDE = DQ_xls.at[i,'CDE']
    this_version = DQ_xls.at[i,'Version Control']
    
    if str(this_filtername)=='nan':
        this_filtername = ''
        this_filtername_for_rulecode = '' 
    else:
        this_filtername = str(this_filtername)
        #this_filtername_for_rulecode = '[' +str(this_filtername)+']'
        #this_filtername_for_rulecode = ' ' + this_filtername +' for table ' + this_tablename
        this_filtername_for_rulecode = ' ' + this_filtername
    
    #for each column that represents a rule (per the manually defined list of rules)
    for rule in rule_col_list:
        
        #no rule for blank cells
        if not str(DQ_xls.at[i,rule])=='nan':
            
            #if there is ")," then we split one cell into 2+ rules
            for rule_param in DQ_xls.at[i,rule].split('),'):
                this_rule = rule
                this_parameter = str(rule_param + ")").replace('))', ')').strip()
                
                #write the parameter values into the rule codes 
                for param in param_col_list:
                    this_parameter = this_parameter.replace(param,str(DQ_xls.at[i,param]))
                this_CTR_rulecode = this_tablename + '.' + this_columnname + '.' + this_rule + this_parameter + this_filtername_for_rulecode
                
                DQ_out.loc[DQ_out.shape[0]+1] = [this_tablename, 
                                                this_filtername,
                                                this_columnname,
                                                this_rule,
                                                this_parameter,
                                                this_CTR_rulecode,
                                                this_CDE,
                                                this_version]
    
#outer-join the IA RuleCode to the CTR RuleCode
#DQ_RuleMap.drop([col for col in DQ_RuleMap.columns if col not in ['CTR Rule Code','IA Rule Code']],inplace=True,axis=1)
DQ_out = pd.merge(DQ_out,DQ_RuleMap,how='left',on=[u'CTR Rule Code'])

#outer-join the rule attributes
DQ_out = pd.merge(DQ_out,DQ_RuleLibrary,how='left',on=[u'DQ Rule Name'])

#rename columns to match Ken's template
for rename_pair in rename_list:
    DQ_out.rename(columns={rename_pair[0]:rename_pair[1]}, inplace=True)

#add hardcoded columns to match Ken's template
for hardcoded_pair in hardcoded_value_list:
    DQ_out[hardcoded_pair[0]] = [hardcoded_pair[1] for i in DQ_out.index]

#write to Excel
DQ_out.to_excel(pd.ExcelWriter(out_folder + out_file), sheet_name = 'IA Rule List', index = False, columns = out_cols)
    
        
print('done DQ_Rules_to_pivot')       
print out_folder+out_file

    