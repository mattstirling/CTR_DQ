'''
Created on Nov 13, 2015

@author: mstirling
'''

import cx_Oracle,glob,os

#open vm db connecttion  
conn = cx_Oracle.connect('ctrmso/password@10.6.134.243:1527/orcl')    
cursor = conn.cursor ()  
os.chdir("c:/temp/python/out/SQL/2016-02-23 W2 R7 IST/")

#loop dir with txt file
for file in glob.glob("*.txt"):
    print file
    for line in open(file):  
        print line.strip()
        cursor.execute(line.strip())  
        conn.commit()
        print line + " commit"
#close connection
cursor.close () 
conn.close ()  