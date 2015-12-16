'''
18-Aug-2015
mstirling

Read values from the many files into a dataframe because it is easy to write values from dataframe into xls
'''

#import libraries
import os

#initialize variables
bListFiles = 1
bRemoveDuplicateCols = 1
readin_folder = 'C:/IBM/InformationServer11-5/ASBNode/bin/Result/'
in_folder = 'C:/Temp/python/in/'
in_file = 'Test_Cases_MR_CTR_DQ v0 7 2015-11-16.xlsx'
out_folder = 'C:/Temp/python/out/'
out_file = 'DQ_summary_outcomes.csv'

if bListFiles:
    
    f_out = open(out_folder + out_file,'w')
    f_out.write('tablename'
                +',columnname'
                +',rulename'
                +',num_records'
                +',num_pass'
                +',num_fail'
                +',filename'
                +'\n')
    
    #for every file in the folder
    for (dirpath, dirnames, filenames) in os.walk(readin_folder):
        
        for filename in filenames:
            
            #if filename contains '_detailresult', then get results
            if '_summaryresult.txt' in filename:

                #if filename is bigger than 0k
                if os.path.getsize(readin_folder + filename)>0:
                    
                    #get information about the file
                    this_tablename = filename.split('.')[1].replace('MKTR_CTR_','')
                    this_columnname = filename.split('.')[2]
                    this_rulename = filename.split('.')[3].replace('_detailresult','')
                    
                    #open the file, read line 1 as a header, all other as body
                    with open(readin_folder + filename,'r') as f:
                        while True:
                            line=f.readline()
                            if not line: break
                            if line.rstrip() == 'Rule Execution History:':
                                header_list = f.readline().rstrip().split(',')
                                values_list = f.readline().rstrip().split(',')
                                break
                    
                    #get the passes and fails
                    num_records = values_list[header_list.index('nbOfRecords')]
                    num_pass = values_list[header_list.index('nbPassed')]
                    num_fail = values_list[header_list.index('nbFailed')]
                    
                    f_out.write(this_tablename)
                    f_out.write(',' + this_columnname)
                    f_out.write(',' + this_rulename)
                    f_out.write(',' + num_records)
                    f_out.write(',' + num_pass)                
                    f_out.write(',' + num_fail)
                    f_out.write(',' + filename)
                    f_out.write('\n') 
          
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'done, wrote sheetnames from ' + str(in_folder) + ' to ' + str(out_folder) + str(out_file)

