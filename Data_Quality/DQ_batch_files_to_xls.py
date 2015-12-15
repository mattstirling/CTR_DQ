'''
18-Aug-2015
mstirling

Read values from the many files into a dataframe because it is easy to write values from dataframe into xls
'''

#import libraries
import os
import pandas as pd

#initialize variables
bListFiles = 1
bRemoveDuplicateCols = 1
in_folder = 'C:/IBM/InformationServer11-5/ASBNode/bin/Result - Copy/'
out_folder = 'C:/Temp/python/out/'
out_file = 'DQ_outcomes.xls'


if bListFiles:
    
    #for every file in the folder
    for (dirpath, dirnames, filenames) in os.walk(in_folder):
        
        #create a dataframe to store each line from each file
        df = pd.DataFrame(columns = ['filename','tablename','header_or_body','values'])
                    
        for filename in filenames:
            
            #if filename contains '_detailresult', then get results
            if '_detailresult.txt' in filename:

                #if filename is bigger than 0k
                if os.path.getsize(in_folder + filename)>0:
                    
                    #open the file, read line 1 as a header, all other as body
                    f = open(in_folder + filename,'r')
                    
                    #read line 1 as a header
                    #for each record, drop the first column - it is a duplicated column
                    #replace '_detailresult' with ''
                    #this_filename = filename.replace('_detailresult.txt','')
                    this_tablename = filename.split('.')[1].replace('MKTR_CTR_','')
                    this_line = f.readline().strip()
                    test = this_line
                    if bRemoveDuplicateCols:
                        remove_cols = 0
                        
                        if ',' not in this_line:
                            break
                        
                        while this_line[:5]=='field':
                            this_line = this_line[this_line.find(',')+1:]
                            remove_cols += 1
                    
                    #print (df.shape[0]+1,this_filename, this_tablename,'header',this_line)
                    df.loc[df.shape[0]+1] = [filename, this_tablename,'header',this_line]
                    
                    for line in f:
                        #read all lines after the 1st as the body
                        #for each record, drop the first column - it is a duplicated column
                        this_line = line.strip()
                        if bRemoveDuplicateCols:
                            for i in xrange(remove_cols):
                                this_line = this_line[this_line.find(',')+1:]
                        #print (df.shape[0]+1,this_filename, this_tablename,'body',this_line)
                        df.loc[df.shape[0]+1] = [filename, this_tablename,'body',this_line]
                    
    #create a column for each table, e.g. 'MKTR_CTR_BOND_L'
    #write out all DQ fails per each table into one xls sheet, e.g. 'MKTR_CTR_BOND_L'
    with pd.ExcelWriter(out_folder + out_file) as writer:
        for tablename in pd.Series(df['tablename']).unique():
            df[df['tablename']==str(tablename)].to_excel(writer, sheet_name = str(tablename), index = False)
          
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'done, wrote sheetnames from ' + str(in_folder) + ' to ' + str(out_folder) + str(out_file)
print len('_detailresult')
