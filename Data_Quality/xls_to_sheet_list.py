'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd, time

in_folder = 'C:/Temp/python/in/CTR Specs/'
out_folder = 'C:/Temp/python/out/'
in_file_list = ['CTR_Inbound_Domains.xlsx',
                'CTR_Inbound_Mapping_(Original_Format)v1.50.xlsx',
                'CTR_Inbound_Mapping_(Original_Format)v1.60.xlsx',
                'CTR_Inbound_Mapping_v1.61.xlsx',
                'CTR_Inbound_Mapping_v1.70.xlsx',
                'CTR_Inbound_Mapping_v1.80.xlsx',
                'CTR_Outbound_Mapping.xlsx',
                'Outbond Mapping- Lancelot Reference Data.xlsx']

f = open(out_folder + 'out_xls_to_sheetnames_' + time.strftime("%Y%m%d") + '.csv','w')

#for every xls
for filename in in_file_list:
    xls = pd.ExcelFile(in_folder + filename)
    #for every landing and extract table
    for sheet_name in xls.sheet_names:
        f.write(filename)
        f.write(',' + sheet_name)
        f.write('\n')

print 'done, wrote sheetnames from ' + str(in_folder) + ' to ' + out_folder + 'out_xls_to_sheetnames_' + time.strftime("%Y%m%d") + '.csv'