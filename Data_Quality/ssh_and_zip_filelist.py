'''
18-Aug-2015
mstirling

'''

#import libraries
import paramiko
from zipfile import ZipFile
from os.path import isfile
from itertools import islice

#initialize variables
bListSSHFiles = 1
bGetSSHFileVersion = 1
bDownloadSSHFile = 1
bListZipFiles = 1


#folder data
out_folder = 'C:/Temp/python/out/'
out_file = 'server_and_zip_file_list.txt'
in_folder = 'C:/Temp/python/in/'
in_zipfile = 'compress/ctrdata-data_out-26-NOV-15-1448662274.zip'
zip_folders = ['outfiles/riskwatch/','outfiles/lancelot/']

#server data
pass_file = 'ctr_unix_prd.txt'
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/infiles/', '/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/']

#filter data
filter_filedate = '20151126'
filter_filetype_list = ['.csv']
filter_ignored_loan_systems = ['SILOPICS_','BM_','GBOS_','WSSMM_','ACBS_']

def format_ctr_file(filename):
    #assume every file ends: ..._D_2015mmdd_...
    #updated to handle CTR_ANVILNY_Trade_20151126_1.csv
    str_temp = filename[:(str(filename).index('_'+filter_filedate))].rstrip('_')
    str_temp = str_temp.rstrip('_D')
    str_temp = str_temp.rstrip('_')
    if 'OBJCHARLIE' in str_temp:
        #remove the ** from OBJCHARLIE**
        n = str_temp.index('OBJCHARLIE')
        str_temp = str_temp[:n+10] + str_temp[n+12:]  
    return str_temp

def ctr_file_version(filepath):
    #open the file and look for a Parent row
    with open(filepath, 'r') as CTR_file:
        for CTR_line in islice(CTR_file, 0, 100):
            num1 = 2 + CTR_line.find('P,')
            if num1 > 1:
                num2 = num1 + CTR_line[num1:].strip().find(',')
                return (CTR_line[num1:num2])

#get password for server
f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

#
# main program - get reference data about files on the server
#
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp
if bListSSHFiles:
    
    #connect to the server
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ctr_host, username=ctr_username, password=ctr_pass)
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    sftp = ssh.open_sftp()
    
    #open file to write to
    f_out = open(out_folder + out_file,'w')
    
    #for both the in-folder and the out-folder
    for server_path in server_path_list:
        
        #get the files we are interested in
        serverfile_list = sftp.listdir(path=server_path)
        for server_file in serverfile_list:
            
            #filter for 1 date
            #filter by filetype extension
            if filter_filedate in server_file and server_file[-4:] in filter_filetype_list:
                
                #filter out loan files
                if sum([1 for i in filter_ignored_loan_systems if i in server_file ])==0: 
                    f_out.write(server_path)
                    f_out.write(',' + str(server_file)) 
                    f_out.write(',' + format_ctr_file(str(server_file)) ) 
                    f_out.write(',' + str(sftp.lstat(server_path + server_file).st_size))
                    
                    if bGetSSHFileVersion:
                        #we save the files in out_folder
                        if isfile(out_folder + str(server_file)):
                            try: f_out.write(',' + ctr_file_version(out_folder + str(server_file)))
                            except: pass
                        elif bDownloadSSHFile:
                            #download the file if we don't already have it downloaded
                            print 'saving ' + str(server_file)
                            sftp.get(server_path + str(server_file), out_folder + str(server_file))
                            try: f_out.write(',' + ctr_file_version(out_folder + str(server_file)))
                            except: pass
                    f_out.write('\n')
           
    if bListZipFiles:
        #read zipfiles
        f_zip = ZipFile(in_folder + in_zipfile,'r')
        
        #for each filename in the folder
        for z_filename in f_zip.namelist():
            for zip_folder in zip_folders:
                if zip_folder in z_filename:
                    if not str(z_filename)==zip_folder:
                        if filter_filedate in z_filename and str(z_filename)[-4:] in filter_filetype_list:
                            f_out.write(zip_folder)
                            f_out.write(',' + str(z_filename).replace(zip_folder,''))
                            f_out.write(',' + format_ctr_file(str(z_filename).replace(zip_folder,'')))
                            f_out.write(',' + str(f_zip.getinfo(z_filename).file_size)) 
                            
                            #not possible to get file version from the outbound files
                            
                            f_out.write('\n')
                            
                            
    f.close()    
    sftp.close()
    ssh.close()
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'output to '+out_folder + out_file

