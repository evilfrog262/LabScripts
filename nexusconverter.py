#!/usr/bin/env python

import sys

#turns Mauve output (exported SNPs) into a nexus file for input to Splitstree4

#determines whether a SNP is valid
def snpValidity(SNP) :
    isValid = False
    length = len(SNP)
    for i in range(length) :
        for j in range (length - 1) :
            if (SNP[i] != SNP[j + 1] and SNP[i] != "-" and SNP[i] != "N" and
                SNP[j + 1] != "-" and SNP[j + 1] != "N") :
                isValid = True
    return isValid



#check for correct commandline arguments
if len(sys.argv) != 4 :
	print("Usage:  nexusconverter.py  <input file>  <outputfile>  <number of samples>")
	sys.exit(0)

InFileName = sys.argv[1]   #Mauve output file
OutFileName = sys.argv[2]  #Nexus format
Columns = int(sys.argv[3]) #Number of columns in Mauve output (number of reads)

InFile = open(InFileName, 'r')	#access the file to be read from
OutFile = open(OutFileName, 'w') #overwrite what is present in the file

LineNumber = 0
ReadCount = 1 
SNPlist = []
SNPrejects = []


#make a list of all the valid SNPs in the file
for Line in InFile:
    if LineNumber == 0 :
        Header = Line.strip('\n')
	ReadNames = Header.split('\t')
    if LineNumber > 0 :	
        Line = Line.strip('\n')
        Line = Line.upper()
        WordList = Line.split('\t')
        wholeSNP = WordList[0]
	SNP = wholeSNP		
        #check validity of the SNP
	if (snpValidity(wholeSNP)) :    #CHECK THIS! DO WE WANT TO INCLUDE THE REF GENOME?
            SNPlist.append(SNP)
        else :
            SNPrejects.append(SNP)
    LineNumber = LineNumber + 1

#write file header
OutFile.write("#NEXUS" + "\n\n" + "Begin DATA;" + "\n\t" + "Dimensions ntax=" +
	str(Columns) + " nchar=" + str(len(SNPlist)) + ";" + "\n\t" + "Format datatype=DNA gap=-;" 
	+ "\n\t" + "Matrix" + "\n")

print(SNPlist[0])

#write all of the SNPs into the new file
for i in range(len(SNPlist[0])) :
    OutFile.write(ReadNames[ReadCount] + '\n')
    ReadCount = ReadCount + 1
    for j in range(len(SNPlist)) :
         OutFile.write(SNPlist[j][i])
    OutFile.write('\n')
    
OutFile.write(";" + "\n" + "END;")

InFile.close()
OutFile.close()
