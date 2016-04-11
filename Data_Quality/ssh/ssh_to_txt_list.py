'''
Created on Feb 29, 2016

@author: mstirling
'''
import paramiko

#variable
b_print_filenames = 1

#folder data
in_folder = 'C:/Temp/python/in/'
pass_file = 'Ref Data/ctr_unix_prd.txt'
#pass_file = 'Ref Data/rw_unix.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'ssh_to_txt_filelist.txt'

#server data
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/riskwatch/']

#filter data
filter_filedate = '20160330'
filter_system = 'GSBL'

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

#open file to write to
f_out = open(out_folder + out_file,'w')

#for both the in-folder and the out-folder
for server_path in server_path_list:
    
    #get the files we are interested in
    serverfile_list = sftp.listdir(path=server_path)
    for server_file in serverfile_list:
        
        
        b_include_file = 1
        
        #filter for 1 date
        if not filter_filedate == '':
            if filter_filedate not in server_file: b_include_file = 0 
        
        #filter by system
        if not filter_system == '':
            if filter_system not in server_file: b_include_file = 0 
        
        if b_include_file:
            
            f_out.write(server_path)
            f_out.write(',' + str(server_file)) 
            f_out.write('\n')
            
            if b_print_filenames: print server_file
                
    print 'got server files'

print 'done'  
                