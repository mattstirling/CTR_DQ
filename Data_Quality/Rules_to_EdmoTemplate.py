'''
Created on Sep 22, 2015

@author: mstirling
'''
import pandas as pd


bWriteReport = 1

sFilePath = 'C:/Users/mstirling/Desktop/Shared/for Ken Lu/MR_CTR_DQ_Rules v0 7 2015-10-05.xlsx'
destination = 'C:/Users/mstirling/Desktop/Shared/for Ken Lu/out/'

DQ_Rules = pd.read_excel(sFilePath,'CTR DQ Rules', header = 0, parse_cols=12)
CDE_data = pd.read_excel(sFilePath,'CDE List', header = 0, parse_cols=7)
CTR_Physical_Data = pd.read_excel(sFilePath,'CTR Spec to Physical Map', header = 0, parse_cols=7)
CTR_Table_Data = pd.read_excel(sFilePath,'CTR Table Metadata', header = 0, parse_cols=6)
CTR_RuleSource_data = pd.read_excel(sFilePath,'Source of DQ Rules - CM', header = 1, parse_cols=26)

#concatenate the cells into one rule expression per each row
aTemp = []
for i in range(len(DQ_Rules.index)):
    sTemp = ''
    if not pd.isnull(DQ_Rules[u'DQ Rule Name'][i]):
        if not pd.isnull(DQ_Rules[u'CTR Table Filter'][i]):
            sTemp = "[" + str(DQ_Rules[u'CTR Table Filter'][i]) + "]"
        sTemp = sTemp + str(DQ_Rules[u'DQ Rule Name'][i]) + str(DQ_Rules[u'DQ Rule Metadata'][i])
    aTemp.append(sTemp)

#add the rule expression to the DQ_Rules Dataset
DQ_Rules['DQ Complete Rule'] = pd.Series(aTemp, index = DQ_Rules.index )

#pivot the DQ_Rules data
DQ_Pivot=pd.pivot_table(DQ_Rules,index=[u'CDE',u'CTR Table Name',u'CTR Physical Column Name'],values=['DQ Complete Rule'],
               columns=[u'Dimension'],aggfunc=lambda x: "%s" % ', '.join(x),fill_value='')
print len(DQ_Pivot.index)

#rename the columns to the dimension
DQ_Pivot.columns = [b for (a,b) in DQ_Pivot.columns]

#add index to the dataframe
DQ_Pivot[u'CDE'] = [a for (a,b,c) in DQ_Pivot.index]
DQ_Pivot[u'CTR Table Name'] = [b for (a,b,c) in DQ_Pivot.index]
DQ_Pivot[u'CTR Physical Column Name'] = [c for (a,b,c) in DQ_Pivot.index]

#add threshold values
DQ_Pivot[u'Accuracy Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Completeness Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Comprehensiveness Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Integrity Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Latency Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Logic Reasonableness Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Recency Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Timeliness Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Uniqueness Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]
DQ_Pivot[u'Validity Threshold'] = ['GREEN >98%, YELLOW <98% and >96%, RED <96%' for i in range(len(DQ_Pivot.index))]

print len(DQ_Pivot.index)

#merge CDE_data
DQ_Pivot = pd.merge(DQ_Pivot,CDE_data, how='left',on=u'CDE')
print len(DQ_Pivot.index)

#merge physical data
DQ_Pivot = pd.merge(DQ_Pivot,CTR_Physical_Data,how='left',on=[u'CTR Table Name',u'CTR Physical Column Name'])
print len(DQ_Pivot.index)

#merge table data
DQ_Pivot = pd.merge(DQ_Pivot,CTR_Table_Data,how='left',on=[u'CTR Table Name'])
print len(DQ_Pivot.index)

#aggregate together the source business description of the business rules
#merge DQ_Rules with CTR_RuleSource_data, aggregate 'Data Quality Rule' by CDExTable, then merge to DQ_Pivot
CTR_RuleSource_data = pd.merge(DQ_Rules,CTR_RuleSource_data,how='left',on=[u'Source Rule Id'])
CTR_RuleSource_Pivot = pd.pivot_table(CTR_RuleSource_data,index=[u'CDE',u'CTR Table Name'],values=['Data Quality Rule'],
               aggfunc=lambda x: "%s" % ',\n '.join(x),fill_value='')
CTR_RuleSource_Pivot[u'CDE'] = [a for (a,b) in CTR_RuleSource_Pivot.index]
CTR_RuleSource_Pivot[u'CTR Table Name'] = [b for (a,b) in CTR_RuleSource_Pivot.index]
DQ_Pivot = pd.merge(DQ_Pivot,CTR_RuleSource_Pivot,how='left',on=[u'CTR Table Name',u'CDE'])
print len(DQ_Pivot.index)
print CTR_RuleSource_Pivot.columns

#DQ_Pivot2=pd.DataFrame(np.array([(a,b,c) for (a,b,c) in DQ_Pivot.index]),columns = [u'CDE',u'CTR Table',u'CTR Attribute'])

#DQ_Pivot[u'CDE'] = pd.Series(DQ_Pivot2[u'CDE'], index = DQ_Pivot.index) 

#print pd.Series(DQ_Pivot2[u'CDE'])

#print DQ_Pivot2[u'CDE']
#print DQ_Pivot.columns

'''
for col in DQ_Pivot.columns:
    DQ_Pivot2[col[1]] = pd.Series(DQ_Pivot[col],index = DQ_Pivot2.index )
    print DQ_Pivot[col]
'''

#print DQ_Pivot2
#print DQ_Pivot.index.get_level_values(u'CTR Table')


#add the CDE metadata to the DQ_Pivot
#DQ_Pivot[u'CDE #'] = pd.Series([CDE_data[u'CDE #'][1] for CTR_Table in DQ_Pivot.index.get_level_values(u'CTR Table')])
#DQ_Pivot[u'CDE #'] = [CDE_data[u'CDE #']CTR_Table for CTR_Table in DQ_Pivot.index.get_level_values(u'CTR Table')]

#print DQ_Pivot.index
#print DQ_Pivot[u'CDE #']
#print CDE_data[u'CDE #'][1]

#rename columns as needed
DQ_Pivot.rename(columns={u'CDE':u'LOGICALNAME Business - Defined'}, inplace=True)
DQ_Pivot.rename(columns={u'Data Quality Rule':u'DATA QUALITY BUSINESS RULE'}, inplace=True)

"Standardized Principle / Measure Name (CBA) & Bank Specific"


write_columns = [u'CDE #', u'CDE REG NUMBER (Assigned by EDMO)', u'BUSINESS GLOSSARY DEFINATION', u'Standardized Principle / Measure Name (CBA) & Bank Specific', 
                 u'Limitations/Commentary/CCR', u'CDE NAME', u'DATA QUALITY BUSINESS RULE', u'CTR Spec Name', u'DATA QUALITY STAGE (ER)', u'LOGICALNAME Business - Defined', 
                 u'CTR Table Name',u'CTR Physical Column Name', u'CTR Data Type', u'Completeness', u'Completeness Threshold', u'Uniqueness', u'Uniqueness Threshold', u'Validity', u'Validity Threshold', u'Logic Reasonableness', 
                 u'Logic Reasonableness Threshold', u'Accuracy', u'Accuracy Threshold', u'Integrity', u'Integrity Threshold', u'Timeliness', u'Timeliness Threshold',
                 u'Recency ', u'Recency Threshold', u'Latency ', u'Latency Threshold', u'Coverage', u'Coverage Threshold', u'Comprehensiveness',
                 u'Comprehensiveness Threshold']

sort_columns = [u'CDE #',u'DATA QUALITY STAGE (ER)',u'CTR Table Name',u'CTR Physical Column Name']
DQ_Pivot.sort(sort_columns, inplace = True)

if bWriteReport:
    with pd.ExcelWriter(destination + 'report.xlsx') as writer:
        #DQ_Rules.to_excel(writer, sheet_name = 'DQ Rough', index = False) 
        DQ_Pivot.to_excel(writer, sheet_name = 'DQ Summary Report', index = False, merge_cells = False,
                          columns = write_columns)
        
print('done DQ_Rules_to_pivot')        

    