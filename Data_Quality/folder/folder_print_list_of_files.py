'''
18-Aug-2015
mstirling

'''

b_write_to_txt = 0
b_write_to_screen = 1

#import libraries
import os

bListFiles = 1
#in_folder = 'C:/Temp/python/ctrdata-data_out-27-OCT-15-1446047665/outfiles'
in_folder = 'C:/Users/mstirling/Desktop/Shared/forTFRM/MMI 20160304/'
#in_folder = 'C:/Temp/python/in/CTR Specs/'
out_folder = 'C:/Temp/python/out/'
out_file = 'CTR_file_list.txt'

#get the files we are interested in
if b_write_to_txt: f = open(out_folder + out_file,'w')
CTR_filelist = []
for (dirpath, dirnames, filenames) in os.walk(in_folder):
    for filename in filenames:
        
        #only grab files with the inclusion date
        #if included_date in filename:
        CTR_filelist.extend(filename)
        if b_write_to_txt: f.write(str(filename) + '\n') # python will convert \n to os.linesep
        if b_write_to_screen: print filename 
        
if b_write_to_txt: f.close()    

#print CTR_filelist
print 'done, wrote files from ' + str(in_folder) + ' to ' + str(out_folder) + str(out_file)

