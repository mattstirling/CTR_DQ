'''
Created on Nov 13, 2015

@author: mstirling
'''

import cx_Oracle,glob,os

#open vm db connecttion  
conn = cx_Oracle.connect('ctrmso/password@192.168.56.10/orcl')    
cursor = conn.cursor ()  
os.chdir("c:/temp/python/out")

#loop dir with txt file
for file in glob.glob("*.txt"):
    print file
    for line in open(file):  
        cursor.execute (line)  
        conn.commit()
        print line + " commit"
#close connection
cursor.close () 
conn.close ()  