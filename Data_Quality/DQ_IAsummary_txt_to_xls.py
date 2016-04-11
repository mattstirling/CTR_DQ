'''
18-Aug-2015
mstirling

Read values from the many files into a dataframe because it is easy to write values from dataframe into xls
'''

#import libraries
import os
import time
import pandas as pd

#readin_folder = 'C:/IBM/InformationServer11-5/ASBNode/bin/Result/'
readin_folder = 'C:/IBM/InformationServer11-5/ASBNode/bin/Result/'
in_folder = 'C:/Temp/python/in/'
out_folder = 'C:/Temp/python/out/'
out_file = 'report_DQ_IA_summary_rule_list_' + time.strftime("%Y%m%d") + '.xlsx'

#create a dataframe to store each line from each file
df = pd.DataFrame(columns = ['IA_rulecode',
                            'tablename',
                            'columnname',
                            'description',
                            'parameters',
                            'num_records',
                            'num_pass',
                            'num_fail',
                            'filename'])

f_out = open(out_folder + out_file,'w')

#for every file in the folder
for (dirpath, dirnames, filenames) in os.walk(readin_folder):
    
    for filename in filenames:
        
        #if filename contains '_detailresult', then get results
        if '_summaryresult.txt' in filename:

            #if filename is bigger than 0k
            if os.path.getsize(readin_folder + filename)>0:
                
                #get information about the file
                this_IA_rulecode = filename.replace('_summaryresult.txt','')
                this_tablename = filename.split('.')[1].replace('MKTR_CTR_','')
                this_columnname = filename.split('.')[3]
                this_description = ''
                this_param = ''
                
                #open the file, read line 1 as a header, all other as body
                with open(readin_folder + filename,'r') as f:
                    while True:
                        line=f.readline()
                        if not line: break
                        
                        #look for the line, "Expression,"
                        if len(line) >= 12:
                            if line[:12] == 'Description,':
                                this_description = line[12:].strip()
                        '''
                        #get the param if we are interested
                        if this_expression == 'field1 > field2':
                            if line[:11] == 'Bound Expression,':
                                this_param = line[0-line.rfind('.'):].strip()
                        '''    
                        #look for "Rule Execution History". get the header and first line
                        if line.rstrip() == 'Rule Execution History:':
                            header_list = f.readline().rstrip().split(',')
                            values_list = f.readline().rstrip().split(',')
                            break
                
                #get the passes and fails
                num_records = values_list[header_list.index('nbOfRecords')]
                num_pass = values_list[header_list.index('nbPassed')]
                num_fail = values_list[header_list.index('nbFailed')]
                
                df.loc[df.shape[0]+1] = [this_IA_rulecode,
                                         this_tablename,
                                         this_columnname,
                                         this_description,
                                         this_param,
                                         num_records,
                                         num_pass,
                                         num_fail,
                                         filename]

#write to xls
with pd.ExcelWriter(out_folder + out_file) as writer:
    df.to_excel(writer, sheet_name ='Summary', index = False)                

#print CTR_filelist
print 'done, wrote from ' + str(readin_folder) + ' to ' + str(out_folder) + str(out_file)

