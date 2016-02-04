'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd

bWriteReport = 1

sFilePath = 'C:/Temp/python/in/MR_CTR_DQ_Rules v2 1 2015-12-03.xlsx'
destination = 'C:/Temp/python/out/'
out_folder = 'C:/Temp/python/out/'
file_out = 'report_DQ_rule_list.csv'

DQ_xls = pd.read_excel(sFilePath,'DQ Rule List', header = 1)
rule_col_list = ['isNotNull','isGreaterThan','isLessThan','AmtIsLessThan','inDomain']
f = open(out_folder+file_out,'w')

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
    
    for rule in rule_col_list:
        if not str(DQ_xls.at[i,rule])=='nan':
            this_rule = rule
            this_parameter = DQ_xls.at[i,rule]
            
            '''
            df.loc[df.shape[0]+1] = [filename, 
                                    this_tablename,
                                    this_columnname,
                                    this_rulename,
                                    this_unique_id_col_name,
                                    this_unique_id,
                                    this_header,
                                    this_line]
            '''
            f.write(this_tablename)
            f.write(',' + str(this_filtername))
            f.write(',' + str(this_columnname))
            f.write(',' + str(this_rule))
            f.write(',' + str(this_parameter))
            f.write('\n')
    
    #CTR Table Name    CTR Table Filter    CTR Physical Column Name    CDE    isNotNull    isGreaterThan    isLessThan    AmtIsLessThan    inDomain    CURRENCY    START_DATE    VALUATION_DATE    MATURITY_DATE

    
        
print('done DQ_Rules_to_pivot')       
print out_folder+file_out 

    