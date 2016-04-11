'''
Created on Feb 29, 2016

@author: mstirling
'''
import paramiko

#control

#folder data
in_folder = 'C:/Temp/python/in/'
pass_file = 'Ref Data/ctr_unix_prd.txt'
#out_download_folder = 'C:/Users/mstirling/Desktop/Shared/for Leonardo/'
out_download_folder = 'C:/Users/mstirling/Desktop/Shared/for Andre/GSBL TFRM Gap Analysis 20160230/from CTR 20160230/'

#server data
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/riskwatch/']

#filter data - (inclusion filters)
filter_filedate = '20160330'
filter_systemname_list = ['GSBL']

#get password for server
f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

#
# main program
#

#get filenames from ctr unix server
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp

#connect to the server
ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ctr_host, username=ctr_username, password=ctr_pass)
stdin, stdout, stderr = ssh.exec_command('ls -l')
sftp = ssh.open_sftp()

#for each folder on the server
for server_path in server_path_list:
    
    #get the files we are interested in
    serverfile_list = sftp.listdir(path=server_path)
    for server_file in serverfile_list:
        
        b_include_file = 1
        
        #filter for 1 date (inclusion)
        if not filter_filedate == '':
            if not filter_filedate in server_file:b_include_file = 0
        
        #filter for source system (inclusion)
        if not filter_systemname_list[0] == '':
            if sum([1 for sys in filter_systemname_list if sys in server_file])==0:b_include_file = 0
        
        if b_include_file:
            print 'saving ' + str(server_file)
            sftp.get(server_path + str(server_file), out_download_folder + str(server_file))
            
print 'got server files from ' + server_path

print 'done'  
                