'''
Created on Feb 29, 2016

@author: mstirling
'''
import paramiko

#folder data
in_folder = 'C:/Temp/python/in/'
#pass_file = 'ctr_unix_prd.txt'
pass_file = 'Ref Data/rw_unix.txt'
out_folder = 'C:/Temp/python/out/'
out_file = 'ssh_to_txt_filelist.txt'

#server data
server_path_list = ['/opt/bns/energy_windows/integration/data/fi/mmi/in/archive/']

#filter data
filter_filedate = '20160308'

#get password for server
f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

#
# main program
#


import pxssh
s = pxssh.pxssh()
if not s.login (ctr_host, ctr_username, ctr_pass):
    print "SSH session failed on login."
    print str(s)
else:
    print "SSH session login successful"
    s.sendline ('ls -l')
    s.prompt()         # match the prompt
    print s.before     # print everything before the prompt.
    s.logout()


print 'done'  
                