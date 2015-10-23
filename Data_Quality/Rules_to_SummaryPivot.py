'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd

#import numpy as np

bWriteReport = 1

sFilePath = 'C:/Temp/python/in/MR_CTR_DQ_Rules v0 8 2015-10-13.xlsx'
destination = 'C:/Temp/python/out/for Ken Lu/out/'

DQ_Rules = pd.read_excel(sFilePath,'CTR DQ Rule List', header = 0, parse_cols=12, nrows = 50)
#DQ_Rules['DQ Complete Rule'] = pd.Series(DQ_Rules[u'CTR Attribute'] + "." + DQ_Rules[u'DQ RuleName'] + DQ_Rules[u'DQ Rule Metadata'], index = DQ_Rules.index )


aTemp = []
for i in range(len(DQ_Rules.index)):
    sTemp = ''
    if not pd.isnull(DQ_Rules[u'DQ Rule Name'][i]):
        if not pd.isnull(DQ_Rules[u'CTR Table Filter'][i]):
            sTemp = "[" + str(DQ_Rules[u'CTR Table Filter'][i]) + "]"
        sTemp = sTemp + str(DQ_Rules[u'CTR Physical Column Name'][i]) + "." + str(DQ_Rules[u'DQ Rule Name'][i]) + str(DQ_Rules[u'DQ Rule Metadata'][i])
    aTemp.append(sTemp)

DQ_Rules['DQ Complete Rule'] = pd.Series(aTemp, index = DQ_Rules.index )

#print(DQ_Rules['DQ Complete Rule'])

#print DQ_Rules['DQ Complete Rule']
DQ_Pivot=pd.pivot_table(DQ_Rules,index=[u'CTR Table Name',u'CDE'],values=['DQ Complete Rule'], 
               columns=[u'EDMO Dimension'],aggfunc=lambda x: "%s" % ', '.join(x),fill_value='')

if bWriteReport:
    with pd.ExcelWriter(destination + 'report.xlsx') as writer:
        DQ_Rules.to_excel(writer, sheet_name = 'DQ Rough', index = False) 
        DQ_Pivot.to_excel(writer, sheet_name = 'DQ Summary Report', index = True)
        
print('done DQ_Rules_to_pivot')        

    