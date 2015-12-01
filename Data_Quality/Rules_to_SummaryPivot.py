'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd

bWriteReport = 1

sFilePath = 'C:/Temp/python/in/MR_CTR_DQ_Rules v0 10 2015-11-24.xlsx'
destination = 'C:/Temp/python/out/'
file_out = 'report_DQ_pivot.xlsx'

DQ_Rules = pd.read_excel(sFilePath,'CTR DQ Rule List', header = 0, parse_cols=12)

aTemp = []
for i in range(len(DQ_Rules.index)):
    sTemp = ''
    if not pd.isnull(DQ_Rules[u'DQ Rule Name'][i]):
        sTemp = "[" + str(int(DQ_Rules[u'CTR DQ Rule Id'][i])) + "]"
        if not pd.isnull(DQ_Rules[u'CTR Table Filter'][i]):
            sTemp += "[" + str(DQ_Rules[u'CTR Table Filter'][i]) + "]"
        sTemp += str(DQ_Rules[u'CTR Physical Column Name'][i]) + "." + str(DQ_Rules[u'DQ Rule Name'][i]) + str(DQ_Rules[u'DQ Rule Metadata'][i])
    aTemp.append(sTemp)

DQ_Rules['DQ Complete Rule'] = pd.Series(aTemp, index = DQ_Rules.index )

DQ_Pivot=pd.pivot_table(DQ_Rules,index=[u'CTR Table Name',u'CDE'],values=['DQ Complete Rule'], 
               columns=[u'EDMO Dimension'],aggfunc=lambda x: "%s" % ', '.join(x),fill_value='')

if bWriteReport:
    with pd.ExcelWriter(destination + file_out) as writer:
        #DQ_Rules.to_excel(writer, sheet_name = 'DQ Rough', index = False) 
        DQ_Pivot.to_excel(writer, sheet_name = 'DQ Summary Report', index = True)
        
print('done DQ_Rules_to_pivot')       
print file_out 

    