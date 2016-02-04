'''
18-Aug-2015
mstirling

Read values from the many files into a dataframe because it is easy to write values from dataframe into xls
'''

#import libraries
import time
import os
import pandas as pd

#initialize variables
bListFiles = 1
bRemoveDuplicateCols = 1
bGetUniqueId = 1
readin_folder = 'C:/IBM/InformationServer11-5/ASBNode/bin/Result/'
in_folder = 'C:/Temp/python/in/'
in_file = 'Test_Cases_MR_CTR_DQ v0 7 2015-11-16_MS added unique id.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'report_DQ_IA_detail_fail_list_' + time.strftime("%Y%mm%dd") + '.xlsx'

if bGetUniqueId:
    #in order to get the unique id, we have to get the name of the unique id column
    #the name of the unique id column is stored in the test cases file
    DQ_Tests = pd.read_excel(in_folder + in_file ,'Expected Outcomes')
    DQ_Tests.drop([col for col in DQ_Tests.columns if col not in ['Table','Unique Record Identifier']],inplace=True,axis=1)
    DQ_Tests.drop_duplicates(inplace=True)
    table_list = [str(x).upper() for x in DQ_Tests['Table'].tolist()]
    id_list = [str(x).upper() for x in DQ_Tests['Unique Record Identifier'].tolist()]
    
if bListFiles:
    
    #for every file in the folder
    for (dirpath, dirnames, filenames) in os.walk(readin_folder):
        
        #create a dataframe to store each line from each file
        df = pd.DataFrame(columns = ['IA_rulecode',
                                     'table name',
                                     'column name',
                                     'filename',
                                     'Unique Record Identifier',
                                     'Id',
                                     'header',
                                     'values'])
                    
        for filename in filenames:
            
            #if filename contains '_detailresult', then get results
            if '_detailresult.txt' in filename:

                #if filename is bigger than 0k
                if os.path.getsize(readin_folder + filename)>0:
                    
                    #open the file, read line 1 as a header, all other as body
                    f = open(readin_folder + filename,'r')
                    
                    #read line 1 as a header
                    #for each record, drop the first column - it is a duplicated column
                    #replace '_detailresult' with ''
                    #this_filename = filename.replace('_detailresult.txt','')
                    this_IA_rulecode = filename.replace('_detailresult.txt','')
                    this_tablename = filename.split('.')[1].replace('MKTR_CTR_','')
                    this_columnname = filename.split('.')[3]
                    try:
                        this_unique_id_col_name = id_list[table_list.index(this_tablename.upper())]
                    except:
                        #tablename is not yet in the testcase file
                        this_unique_id_col_name = ''
                    
                    this_line = f.readline().strip()
                    if bRemoveDuplicateCols:
                        remove_cols = 0
                        
                        if ',' not in this_line:
                            break
                        
                        while this_line[:5]=='field':
                            this_line = this_line[this_line.find(',')+1:]
                            remove_cols += 1
                    
                    #get the header from the first line    
                    #df.loc[df.shape[0]+1] = [filename, this_tablename,'header',this_line]
                    this_header = this_line
                    this_header_list = this_header.split(',')
                    for line in f:
                        #read all lines after the 1st as the body
                        #for each record, drop the first X number of columns - these are the duplicated columns (X = value of "remove_cols" variable)
                        this_line = line.strip()
                        if bRemoveDuplicateCols:
                            for i in xrange(remove_cols):
                                this_line = this_line[this_line.find(',')+1:]
                        
                        #get the unique row id
                        if not this_unique_id_col_name == '':
                            this_line_list = this_line.split(',')
                            this_unique_id = this_line_list[this_header_list.index(this_unique_id_col_name)]
                        else:
                            this_unique_id=''
                        #print ([filename,this_tablename, this_columnname,this_rulename,this_unique_id_col_name,this_unique_id,this_header,this_line])
                        #print (df.shape[0]+1,this_filename, this_tablename,'body',this_line)
                        
                        
                        df.loc[df.shape[0]+1] = [this_IA_rulecode,
                                                 this_tablename,
                                                 this_columnname,
                                                 filename,
                                                 this_unique_id_col_name,
                                                 this_unique_id,
                                                 this_header,
                                                 this_line]
                        
                    
    #create a column for each table, e.g. 'MKTR_CTR_BOND_L'
    #write out all DQ fails per each table into one xls sheet, e.g. 'MKTR_CTR_BOND_L'
    
    with pd.ExcelWriter(out_folder + out_file) as writer:
        df.to_excel(writer, sheet_name ='All Tables', index = False)
        for tablename in pd.Series(df['table name']).unique():
            df[df['table name']==str(tablename)].to_excel(writer, sheet_name = str(tablename), index = False)
          
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'done, wrote sheetnames from ' + str(in_folder) + ' to ' + str(out_folder) + str(out_file)

