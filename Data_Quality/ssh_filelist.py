'''
18-Aug-2015
mstirling

'''

#import libraries
import paramiko
from zipfile import ZipFile

#initialize variables
bGetFile = 0
bListSSHFiles = 1
bFilterFiletype = 1
bListZipFiles = 1

#folder data
in_folder = 'C:/Temp/python/in/'
out_folder = 'C:/Temp/python/out/'
out_file = 'server_file_list.txt'

#server data
pass_file = 'ctr_unix_prd.txt'
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/infiles/', '/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/']

#filter data
filter_filedate = '20151126'
filter_filetype_list = ['.csv','.dat']

def format_ctr_file(filename):
    str_temp = filename.replace(filter_filedate, '')
    

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
    f = open(out_folder + out_file,'w')
    
    #for both the in-folder and the out-folder
    for server_path in server_path_list:
        
        #get the files we are interested in
        serverfile_list = sftp.listdir(path=server_path)
        for server_file in serverfile_list:
            
            #filter for 1 date
            #filter by filetype extension
            if filter_filedate in server_file and server_file[-4:] in filter_filetype_list:
                #if not '.mrk' in server_file:
                f.write(server_path)
                f.write(',' + str(server_file)) 
                f.write(',' + str(server_file).replace(filter_filedate, '') ) 
                f.write(',' + str(sftp.lstat(server_path + server_file).st_size))
                f.write('\n')
        
        #can only get the files if we also list all of them
        if bGetFile:
            for server_file in serverfile_list:
            #if filter_filedate in server_file and server_file[-4:] == filter_Filetype:
                if filter_filedate in server_file:    
                    if not '.mrk' in server_file:
                        if sftp.lstat(server_path + server_file).st_size > 10 * 267403182:
                            print 'saving ' + str(server_file)
                        sftp.get(server_path + str(server_file), out_folder + str(server_file))
    
    if bListZipFiles:
        
                    
    f.close()    
    sftp.close()
    ssh.close()
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'output to '+out_folder + out_file

