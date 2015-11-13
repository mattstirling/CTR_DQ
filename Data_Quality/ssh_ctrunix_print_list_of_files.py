'''
18-Aug-2015
mstirling

Goal is to connect to a ssh server, 
1. to list all files in a given folder 
'''

#import libraries
import paramiko
'''
from dateutil import rrule
from datetime import datetime, timedelta
'''

#initialize variables
bListFiles = 1
bFilterFiletype = 1
filter_Filetype = '.dat' 
#CTR_server_path = '/opt/ctr/ctr/ctrapp/ctr/ctrarchive/infiles/'
CTR_server_path = '/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/'
RW_server_path = '/opt/bns/var_rw/data/riskwatch/wss/fx/'
in_folder = 'C:/Temp/python/in/'
out_folder = 'C:/Temp/python/out/'
out_file = 'CTR_file_list.txt'

pass_file = 'ctr_unix_prd.txt'
server_path = CTR_server_path
filter_filedate = '20151030'

f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

#get the files
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp

if bListFiles:
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ctr_host, username=ctr_username, password=ctr_pass)
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    sftp = ssh.open_sftp()
    
    #get the files we are interested in
    CTR_filelist = []
    serverfile_list = sftp.listdir(path=server_path)
    
    
    f = open(out_folder + out_file,'w')
    for server_file in serverfile_list:
        if filter_filedate in server_file and server_file[-4:] == filter_Filetype:
            
            
            f.write(str(server_file) + '\n') # python will convert \n to os.linesep
            CTR_filelist.append(str(server_file))
        
    f.close()    
    sftp.close()
    ssh.close()
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist
print 'done'

