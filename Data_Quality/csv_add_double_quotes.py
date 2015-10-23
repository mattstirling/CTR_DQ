'''
Created on Oct 2, 2015

@author: mstirling
'''

import csv

newrow = []
csvFolder = 'C:/Users/mstirling/Desktop/Shared/for Ken Lu/Sample Data 23-Sep-2015/'
csvFile = 'RISKWATCH_SBL_EXPOSURE_EXP'
csvFileRead = open(csvFolder + csvFile + '.csv', 'rb')
csvFileNew = open(csvFolder + csvFile + '_formatted.csv', 'wb')

# Open the CSV
csvReader = csv.reader(csvFileRead, delimiter = ',')

# Append the rows to variable newrow
for row in csvReader:
    newrow.append(row)

# Add quotes around the third list item

for row in newrow:
    for i in range(len(row)):
        #row[i] = '\"' + str(row[i]) + '\"'
        row[i] = str(row[i])
    
        

    
csvFileRead.close()

# Create a new CSV file
csvWriter = csv.writer(csvFileNew, delimiter = ',',quoting=csv.QUOTE_ALL ) #, quoting=csv.QUOTE_NONE)

# Append the csv with rows from newrow variable
for row in newrow:
    csvWriter.writerow(row)

csvFileNew.close()

print 'double quotes file done'