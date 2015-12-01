'''
Created on Nov 30, 2015

@author: mstirling
'''
from zipfile import ZipFile

#folder data
in_folder = 'C:/Temp/python/in/'
in_zipfile = 'compress/ctrdata-data_out-26-NOV-15-1448662274.zip'
out_folder = 'C:/Temp/python/out/'
out_file = 'zip_file_list.txt'
zip_folders = ['outfiles/riskwatch/','outfiles/lancelot/']

f_out = open(out_folder + out_file,'w')
f_zip= ZipFile(in_folder + in_zipfile,'r')
   
for z_filename in f_zip.namelist():
    for zip_folder in zip_folders:
        if zip_folder in z_filename:
            if not str(z_filename)==zip_folder:
                f_out.write(str(z_filename).replace(zip_folder,''))
                f_out.write(',' + str(f_zip.getinfo(z_filename).file_size)) 
                f_out.write('\n')
                #print (str(z_filename),f_zip.getinfo(z_filename).file_size)
f_zip.close()


