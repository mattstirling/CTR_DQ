'''
Created on Oct 15, 2015

@author: mstirling
'''
import pandas as pd

#control variables
b_create_insert_sql = 1
b_create_delete_sql = 1

def xls_date_format_to_CTR_format(xls_value,table_name):
    #xls format is yyyy-mm-dd 00:00:00
    yyyy_mm_dd = xls_value[:10].split('-')
    #print yyyy-mm-dd
    
    if table_name[-2:] == '_L':
        #CTR date format is YYYY-MM-DD
        return "'" + yyyy_mm_dd[0] + '-' + yyyy_mm_dd[1] + '-' + yyyy_mm_dd[2] + "'" 
        
    elif table_name[-4:] == '_EXP':
        
        if 'LANCELOT' in table_name.upper():
            #CTR date format is YYYY-MM-DD
            return "'" + yyyy_mm_dd[0] + '-' + yyyy_mm_dd[1] + '-' + yyyy_mm_dd[2] + "'"
        
        elif 'RISKWATCH' in table_name.upper():
            #CTR date format is YYYY/MM/DD
            return "'" + yyyy_mm_dd[0] + '/' + yyyy_mm_dd[1] + '/' + yyyy_mm_dd[2] + "'"
            
def xls2SQL(xls_value, datatype, col_name, table_name):
    #print [table_name,col_name,xls_value]
    if str(xls_value) in ('nan','NaT'):
        return 'null'
        
    dict_case = {
                  'VARCHAR2': 'text',
                  'DATE': 'date',
                  'TIMESTAMP(6)': 'date',
                  'NUMBER': 'number',
                  'CHAR': 'text',
                  'CLOB': 'text'
                  }
    
    datatype_case = dict_case.get(datatype,'text')
    
    #treat dates as text as a special case
    if datatype_case == 'text' and col_name[-5:] == '_DATE':
        return xls_date_format_to_CTR_format(str(xls_value),table_name.upper())
    
    #print [xls_value, datatype, datatype.split("(")[0], datatype_case]
    if datatype_case == 'text':
        return "'" + str(xls_value) + "'"
    elif datatype_case == 'number':
        return str(xls_value)
    elif datatype_case == 'date':
        return "to_date('" + str(xls_value)[:10] + "','yyyy-mm-dd')"
      

#load data from test cases and load the data types
filepath_testcases = 'C:/Temp/python/in/Copy of WAVE 2 Testing v2.xlsx'
filepath_datatypes = 'C:/Temp/python/in/CTR_R7_Datatype_2016-01-21.xlsx'
filefolder_output = 'C:/Temp/python/out/SQL/'

#open the entire xls (to read the filesnames)
xls = pd.ExcelFile(filepath_testcases)
datatype = pd.read_excel(filepath_datatypes,sheetname='Data Type')
#print [sheet_name for sheet_name in xls.sheet_names if (sheet_name[-2:].upper()=='_L') | (sheet_name[-4:].upper()=='_EXP')]

if b_create_insert_sql:
    #for every landing and extract table
    for sheet_name in [sheet_name for sheet_name in xls.sheet_names if (sheet_name[-2:].upper()=='_L') | (sheet_name[-4:].upper()=='_EXP') | (sheet_name[-2:].upper()=='_O')]:
        #read in the Sheet
        sheet = pd.read_excel(filepath_testcases, sheet_name, header=0)
        sheet.columns = [str(col).strip() for col in sheet.columns]
        
        #create a dataframe with the datatype per each column
        DQ_col_datatype = pd.DataFrame([str(sheet_name).upper() for i in sheet.columns],columns=[u'TABLE_NAME'])
        DQ_col_datatype[u'COLUMN_NAME'] = sheet.columns
        DQ_col_datatype = pd.merge(DQ_col_datatype,datatype,how='left',on=[u'TABLE_NAME',u'COLUMN_NAME'])
        DQ_col_datatype.index =sheet.columns
        
        #log the datatype to an excel sheet
        #DQ_col_datatype.to_excel(pd.ExcelWriter(filefolder_output + str(sheet_name).upper() + '.xlsx'), sheet_name = str(sheet_name).upper(), index = False, merge_cells = False)
        
        #create an output file for this xls sheet
        f = open(filefolder_output + sheet_name.upper() + '.txt','w')
        
        #create the first half of the statement from the Header
        SQL_part1 = 'INSERT INTO ' + str(sheet_name) + ' COLUMNS (' + str(', '.join(sheet.columns)) + ')' 
        
        #iterate through the rest of the records. create 1 statement per each record
        for i in sheet.index:
            #print [sheet[col][i] for col in sheet.columns]
            #print [DQ_col_datatype[u'DATA_TYPE'][col] for col in sheet.columns]
            #print [col for col in sheet.columns]
            #print sheet_name
            SQL_part2 = ' VALUES (' + str(', '.join([xls2SQL(sheet[col][i],DQ_col_datatype[u'DATA_TYPE'][col],str(col),str(sheet_name)) for col in sheet.columns])) + ')'
            f.write(SQL_part1 + SQL_part2 + '\n')

if b_create_delete_sql:
    f = open(filefolder_output + 'DELETE_SQL.txt','w')
    for sheet_name in [sheet_name for sheet_name in xls.sheet_names if (sheet_name[-2:].upper()=='_L') | (sheet_name[-4:].upper()=='_EXP') | (sheet_name[-2:].upper()=='_O')]:
        SQL = 'delete from ' + sheet_name + ';'
        f.write(SQL + '\n')
        
print 'done SQL statements'    
print filefolder_output   
    
