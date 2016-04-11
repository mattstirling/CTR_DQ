'''
Created on Nov 30, 2015

@author: mstirling
'''
from zipfile import ZipFile

#folder data
#in_folder = 'C:/Temp/python/in/compress/'
in_folder = 'C:/Users/mstirling/Desktop/Shared/forTFRM/'
in_zipfile_list = ['K2 2016-03-04/20160304_1.zip','K2 2016-03-04/20160304_2.zip','K2 CD 2016-03-04/k2cd_20160304.zip']
out_folder = 'C:/Temp/python/out/'
out_file = 'zip_file_list.csv'

f_out = open(out_folder + out_file,'w')
for in_zipfile in in_zipfile_list:   
    f_zip= ZipFile(in_folder + in_zipfile,'r')
    for z_filename in f_zip.namelist():
        f_out.write(in_zipfile)
        f_out.write(',' + z_filename)
        #f_out.write(',' + str(f_zip.getinfo(z_filename).file_size)) 
        f_out.write('\n')
    f_zip.close()
    print 'done ' + in_folder + in_zipfile
print 'done, out to: ' + out_folder + out_file


