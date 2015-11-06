'''
18-Aug-2015
mstirling

Goal is to connect to a ssh server, 
1. to list all files in a given folder 
'''

#import libraries
import paramiko
from itertools import islice
import os
'''
from dateutil import rrule
from datetime import datetime, timedelta
'''

#initialize variables
bListFiles = 1
bGetFile = 1
CTR_server_path = '/opt/ctr/ctr/ctrapp/ctr/ctrarchive/infiles/'
RW_server_path = '/opt/bns/var_rw/data/riskwatch/wss/fx/'
in_list_filename = 'CTR_CM_File_Types.txt'
CTR_filetype = '.csv'
CTR_date = '20151102'

in_folder = 'C:/Temp/python/in/'
out_folder = 'C:/Temp/python/out/'
pass_file = 'ctr_unix_prd.txt'
out_file = 'CTR_file_list.txt'
out_filename = 'CTR_CM_fileType_list.txt'
out_folder_ken = 'K:/Application Development/DATA/DATALOAD/K2/'


out_folder = out_folder_ken
f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

'''
CTR_system = 'SILOPICS'
CTR_record_type = '_LO_DL'
CTR_dly_mnthly = '_D_'
CTR_filetype = '.csv'

#get the list of dates
CTR_datelist = []
now = datetime.now()
for dt in rrule.rrule(rrule.DAILY, dtstart=now + timedelta(days=-100), until=now):
    CTR_datelist.append(dt.strftime('%Y%m%d'))
'''

#get the files
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp

if bListFiles:
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ctr_host, username=ctr_username, password=ctr_pass)
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    sftp = ssh.open_sftp()
    
    #get the files we are interested in
    serverfile_list = sftp.listdir(path=CTR_server_path)
    #print serverfile_list
    #print len(serverfile_list)
    
    #look at files for only one date
    new_list = []
    for server_file in serverfile_list:
        if CTR_date in server_file:
            new_list.append(server_file)
    serverfile_list = new_list
    #print len(serverfile_list)
    
    #look at files for only one "file extension type"
    new_list = []
    for server_file in serverfile_list:
        if CTR_filetype == server_file[-4:]:
            new_list.append(server_file)
    serverfile_list = new_list
    #print len(serverfile_list)
    
    '''
    if bGetFile:
        #determine the list of files to grab
        #get the unix file via ssh and save locally
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.load_system_host_keys()
        #ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect('ctr-uat.bns', username='mstirl', password='July2015')
        #stdin, stdout, stderr = ssh.exec_command('ls -l')
        sftp = ssh.open_sftp()
        for sFilename in serverfile_list:
            #print source + sFilename
            sftp.get(CTR_server_path + sFilename, out_folder + sFilename)
        sftp.close()
        ssh.close()
        print('got the file')
    else:
        print('did not get file')
    '''
        
    #now get the CTR filelist, and the version for each
    #CTR_filelist = []
    f = open(out_folder + out_file,'w')
    with open(in_folder + in_list_filename, 'r') as infile:
        for line in infile:
            print line.strip()
            
            for server_file in serverfile_list:
                #print server_file
                
                if line.strip() in server_file:
                    
                    #save file
                    if bGetFile:
                        print 'saving ' + str(server_file)
                        sftp.get(CTR_server_path + str(server_file), out_folder + str(server_file))
                    
                    #print str(server_file) + ',' + str(line.strip())
                    f.write(str(server_file) + ',')
                    f.write(str(line.strip()) + ',')
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
                            '''
                            print CTR_line.strip()
                            print str(num1) + ',' + str(num2)
                            print CTR_line.strip()[num1:]
                            print CTR_line[num1:num2] + '\n'
                            '''
                    f.write('\n')
    #close all files
    f.close()    
    sftp.close()
    ssh.close()
    
    #print a helpful message
    print ('got the list of files')
else:
    print ('did not get list of files')

#print CTR_filelist


