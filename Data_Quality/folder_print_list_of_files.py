'''
18-Aug-2015
mstirling

'''

#import libraries
import os

bListFiles = 1
in_folder = 'C:/Temp/python/ctrdata-data_out-27-OCT-15-1446047665/outfiles'
out_folder = 'C:/Temp/python/out/'
out_file = 'CTR_file_list.txt'
included_date = '20151027'

if bListFiles:
    
    #get the files we are interested in
    f = open(out_folder + out_file,'w')
    CTR_filelist = []
    for (dirpath, dirnames, filenames) in os.walk(in_folder):
        for filename in filenames:
            
            #only grab files with the inclusion date
            if included_date in filename:
                CTR_filelist.extend(filename)
                f.write(str(filename) + '\n') # python will convert \n to os.linesep
          
    f.close()    
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'done, wrote sheetnames from ' + str(in_folder) + ' to ' + str(out_folder) + str(out_file)

