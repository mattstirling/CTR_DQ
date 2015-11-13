'''
18-Aug-2015
mstirling

'''

#import libraries
import paramiko
from itertools import islice
import os

def getCTRfiletype(f):
    #assume every file ends: ..._D_2015mmdd_...
    return f[:(str(f).index('_D_201'))].rstrip('_')

#initialize variables
bListFiles = 1
bGetFile = 1
CTR_server_path = '/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/'
RW_server_path = '/opt/bns/var_rw/data/riskwatch/wss/fx/'
#in_list_filetype = 'CTR_CM_File_Types.txt'
in_list_filename = 'CTR_file_list.txt'
CTR_filetype = '.csv'
CTR_date = '20151102'

in_folder = 'C:/Temp/python/in/'
out_folder = 'C:/Temp/python/out/'
pass_file = 'ctr_unix_prd.txt'
out_file = 'CTR_file_list.txt'
out_filename = 'CTR_CM_fileType_list.txt'
out_folder_ken = 'K:/Application Development/DATA/DATALOAD/K2/'


out_folder = out_folder
f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

#get the files
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp
filelist = []

if bListFiles:
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ctr_host, username=ctr_username, password=ctr_pass)
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    sftp = ssh.open_sftp()
    
    #get the files we are interested in
    f = open(in_folder + pass_file,'r')
    for line in f:
        filelist.append(str(line).strip())
        
    #now get the CTR filelist, and the version for each
    f = open(out_folder + out_file,'w')
    with open(in_folder + in_list_filename, 'r') as infile:
        for line in infile:
            server_file = line.strip()
            
            #save file
            if bGetFile:
                print 'saving ' + str(server_file)
                sftp.get(CTR_server_path + str(server_file), out_folder + str(server_file))
            
            #print str(server_file) + ',' + str(line.strip())
            f.write(str(server_file) + ',')
            #f.write(str(getCTRfiletype(server_file)) + ',')
            f.write(str(os.path.getsize(out_folder + str(server_file)))+',')
            #CTR_filelist.append(str(server_file))
        
            #open file
            with open(out_folder + str(server_file), 'r') as CTR_file:
                for CTR_line in islice(CTR_file, 0, 100):
                    num1 = 2 + CTR_line.find('P,')
                    if num1 > 1:
                        num2 = num1 + CTR_line[num1:].strip().find(',')
                        f.write(CTR_line[num1:num2])
                        break
                f.write('\n')
    #close all files
    f.close()    
    sftp.close()
    ssh.close()
    
    #print a helpful message
    print ('got the list of files')
else:
    print ('did not get list of files')

print 'done'


