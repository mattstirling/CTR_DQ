'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd
#import numpy as np

bWriteReport = 1

sFilePath = 'C:/Users/mstirling/Desktop/Shared/for Ken Lu/CTR POC DQ Rules v0 4 2015-09-15.xlsx'
destination = 'C:/Users/mstirling/Desktop/Shared/for Ken Lu/out/'

DQ_Rules = pd.read_excel(sFilePath,'CTR DQ Rules', header = 0, parse_cols=12)
DQ_Rules['DQ Complete Rule'] = pd.Series(DQ_Rules[u'CTR Attribute'] + "." + DQ_Rules[u'DQ RuleName'] + DQ_Rules[u'DQ Rule Metadata'], index = DQ_Rules.index )

print DQ_Rules['DQ Complete Rule']

#print DQ_Rules.groupby(u'CDE')['DQ Complete Rule'].apply(lambda x: x.sum())
#print DQ_Rules.groupby([u'CTR Table',u'CDE'])['DQ Complete Rule'].apply(lambda x: "%s" % ', '.join(x))

DQ_Pivot=pd.pivot_table(DQ_Rules,index=[u'CTR Table',u'CDE'],values=['DQ Complete Rule'],
               columns=[u'Dimension'],aggfunc=lambda x: "%s" % ', '.join(x),fill_value='')
#print DQ_Rules.columns
#print DQ_Rules[u'CTR Attribute']
#print DQ_Rules[u'CTR Attribute'][0]

#DQ_rule_complete = DQ_Rules[u'CTR Attribute'] + "." + DQ_Rules[u'DQ RuleName'] + DQ_Rules[u'DQ Rule Metadata']
'''
for i in range(len(DQ_Rules.index)):
    DQ_rule_complete.append( DQ_Rules[u'CTR Attribute'] + "." + DQ_Rules[u'DQ RuleName'] + DQ_Rules[u'DQ Rule Metadata'])
'''
#print DQ_rule_complete
    
    #[unique, counts] = np.unique(np.reshape(ISL2RO[u'TRANSIT_ACCTG'],(1,len(ISL2RO.index))), return_counts=True)
    #ISL2RO_unique = pd.DataFrame(ISL2RO,columns=[u'ORIG_SRC_SYS_ID',u'TRANSIT_ACCTG']).drop_duplicates()
    #ISL2RO_unique['Source File Date+Type'] = pd.Series([source_filepath_datetype for i in range(len(ISL2RO_unique.index))], index = ISL2RO_unique.index)
    #ISL2RO_ALL_unique = pd.concat([ISL2RO_ALL_unique,ISL2RO_unique])

if bWriteReport:
    with pd.ExcelWriter(destination + 'report.xlsx') as writer:
        DQ_Rules.to_excel(writer, sheet_name = 'DQ Rough', index = False) 
        DQ_Pivot.to_excel(writer, sheet_name = 'DQ Summary Report', index = True)
        
print('done DQ_Rules_to_pivot')        

    