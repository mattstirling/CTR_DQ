'''
Created on Oct 29, 2015

@author: mstirling
'''
import pandas as pd

in_folder = 'C:/Temp/python/in/'
out_folder = 'C:/Temp/python/out/'
filename_CTRspec_160 = 'CTR_Inbound_Mapping_(Original_Format)v1.60.xlsx'
filename_CTRspec_150 = 'CTR_Inbound_Mapping_(Original_Format)v1.50.xlsx'
filename_CTRspec_161 = 'CTR_Inbound_Mapping_v1.61.xlsx'
filename_CTRout = 'CTR_Outbound_Mapping.xlsx'
filename_out_CTRspec_sheet_list = 'CTRspec_sheet_list.txt'

#chose the xls version to look at
filename_CTRspec = filename_CTRspec_150

f = open(out_folder + filename_out_CTRspec_sheet_list,'w')
xls = pd.ExcelFile(in_folder + filename_CTRspec)

#for every landing and extract table
for sheet_name in xls.sheet_names:
    f.write(sheet_name + '\n')


print 'done, wrote sheetnames from ' + str(in_folder) + str(filename_CTRspec) + ' to ' + str(out_folder) + str(filename_out_CTRspec_sheet_list)